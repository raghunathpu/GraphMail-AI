from core.state import EmailState
from agents import (
    filtering_agent,
    summarization_agent,
    response_agent,
    human_review_agent
)

from agents.priority_agent import calculate_priority

from langgraph.graph import END, StateGraph


def supervisor_langgraph(
    email: dict,
    state: EmailState,
    user_name: str,
    recipient_name: str,
    tone: str = "Professional"
) -> EmailState:

    state.current_email = email

    def filtering_node(state: EmailState):

        email = state.current_email

        classification = filtering_agent.filter_email(email)

        email["classification"] = classification

        return state

    def priority_node(state: EmailState):

        email = state.current_email

        priority = calculate_priority(email)

        email["priority"] = priority

        return state

    def summarization_node(state: EmailState):

        email = state.current_email

        analysis = summarization_agent.summarize_email(email)

        email["summary"] = analysis.get("summary", "")

        email["sentiment"] = analysis.get(
            "sentiment",
            "Neutral"
        )

        email["action_items"] = analysis.get(
            "action_items",
            []
        )

        return state

    def response_node(state: EmailState):

        email = state.current_email

        response = response_agent.generate_response(
            email=email,
            summary_data={
                "summary": email.get("summary", ""),
                "sentiment": email.get("sentiment", "Neutral")
            },
            recipient_name=recipient_name,
            your_name=user_name,
            tone=tone
        )

        response = human_review_agent.review_email(
            email,
            response
        )

        email["response"] = response

        state.history.append(
            {
                "email_id": email.get("id"),
                "classification": email.get(
                    "classification"
                ),
                "priority": email.get("priority"),
                "sentiment": email.get(
                    "sentiment"
                )
            }
        )

        return state

    graph_builder = StateGraph(EmailState)

    graph_builder.add_node(
        "filtering",
        filtering_node
    )

    graph_builder.add_node(
        "priority",
        priority_node
    )

    graph_builder.add_node(
        "summary",
        summarization_node
    )

    graph_builder.add_node(
        "response",
        response_node
    )

    def post_filter(state):

        email = state.current_email

        if email.get("classification") == "spam":
            return END

        return "priority"

    graph_builder.add_conditional_edges(
        "filtering",
        post_filter,
        {
            "priority": "priority",
            END: END
        }
    )

    graph_builder.add_edge(
        "priority",
        "summary"
    )

    graph_builder.add_edge(
        "summary",
        "response"
    )

    graph_builder.add_edge(
        "response",
        END
    )

    graph_builder.set_entry_point(
        "filtering"
    )

    graph = graph_builder.compile()

    return graph.invoke(state)
