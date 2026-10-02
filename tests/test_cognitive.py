from src.rebecca.memory import Memory
from src.rebecca.brain import Brain
from src.rebecca.cognitive import CognitiveEngine


def test_cognitive_engine():
    memory = Memory("data/memory/test_rebecca.db")
    brain = Brain()
    cognitive = CognitiveEngine(
        memory,
        brain,
    )

    response = cognitive.respond(
        "¿Cómo te llamas?"
    )

    assert response
    assert isinstance(response, str)
    assert len(response) > 0

    history = cognitive.conversation.get_messages()

    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "¿Cómo te llamas?"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == response

    second_response = cognitive.respond(
        "¿Y cómo se llama mi asistente?"
    )

    assert second_response
    assert isinstance(second_response, str)
    assert len(second_response) > 0

    history = cognitive.conversation.get_messages()

    assert len(history) == 4

    assert history[0]["role"] == "user"
    assert history[0]["content"] == "¿Cómo te llamas?"

    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == response

    assert history[2]["role"] == "user"
    assert history[2]["content"] == (
        "¿Y cómo se llama mi asistente?"
    )

    assert history[3]["role"] == "assistant"
    assert history[3]["content"] == second_response

    memory.close()


if __name__ == "__main__":
    test_cognitive_engine()
    print("Test cognitivo: OK")
