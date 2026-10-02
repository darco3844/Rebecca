from src.rebecca.conversation import Conversation
from src.rebecca.knowledge import Knowledge
from src.rebecca.identity import Identity
from src.rebecca.memory import Memory
from src.rebecca.memory_manager import MemoryManager
from src.rebecca.intent import IntentDetector
from src.rebecca.memory_classifier import MemoryClassifier
from src.rebecca.memory_decision import MemoryDecision
from src.rebecca.episodic_memory import EpisodicMemory
from src.rebecca.working_memory import WorkingMemory
from src.rebecca.task_state import TaskState
from src.rebecca.tool_intent import ToolIntentDetector
from src.rebecca.tools.manager import ToolManager
from src.rebecca.tools.file_path import FilePathExtractor
from src.rebecca.context import ContextBuilder
from src.rebecca.tool_executor import ToolExecutor
from src.rebecca.tool_planner import ToolPlanner
from src.rebecca.plugins.manager import PluginManager


class CognitiveEngine:
    def __init__(
        self,
        memory=None,
        brain=None,
        max_permission="safe",
        conversation=None,
        plugin_modules=None,
    ):
        self.identity = Identity()
        self.knowledge = Knowledge()

        if memory is None:
            memory_database = Memory()
            self.memory = MemoryManager(
                memory_database
            )

        elif isinstance(
            memory,
            MemoryManager,
        ):
            self.memory = memory
            memory_database = memory.memory

        else:
            memory_database = memory
            self.memory = MemoryManager(
                memory_database
            )

        self.brain = brain
        self.max_permission = max_permission

        self.intent = IntentDetector()

        self.classifier = MemoryClassifier()

        self.decision = MemoryDecision(
            classifier=self.classifier
        )

        self.episodes = EpisodicMemory(
            memory_database
        )

        self.working_memory = WorkingMemory()
        self.task_state = TaskState()

        self.tool_intent = ToolIntentDetector()

        self.tools = ToolManager()

        self.plugins = PluginManager(
            self.tools
        )

        self.file_path_extractor = (
            FilePathExtractor()
        )

        if plugin_modules:
            self._load_plugins(
                plugin_modules
            )

        self.tool_planner = None

        if self.brain is not None:
            self.tool_planner = ToolPlanner(
                brain=self.brain,
                tools=self.tools,
            )

        self.tool_executor = ToolExecutor(
            tool_intent=self.tool_intent,
            tools=self.tools,
            file_path_extractor=(
                self.file_path_extractor
            ),
            max_permission=self.max_permission,
            planner=self.tool_planner,
        )

        if conversation is None:
            self.conversation = Conversation()

        else:
            self.conversation = conversation

        self.context = ContextBuilder(
            identity=self.identity,
            knowledge=self.knowledge,
            memory=self.memory,
            working_memory=self.working_memory,
            episodes=self.episodes,
            task_state=self.task_state,
        )

    def respond(self, user_input):
        user_input = user_input.strip()

        if not user_input:
            return "No recibí ningún mensaje."

        if self.tool_planner is None:
            self._ensure_tool_planner()

        tool = self.tool_executor.execute(
            user_input
        )

        system_context = self.context.build(
            user_input,
            tool_context=tool["context"],
            include_extended_context=not tool["used"],
        )

        self.conversation.add_user_message(
            user_input
        )

        messages = [
            {
                "role": "system",
                "content": system_context,
            }
        ]

        messages.extend(
            self.conversation.get_messages()
        )

        response = self._ask_brain(
            messages
        )

        self.conversation.add_assistant_message(
            response
        )

        decision = self.decision.decide(
            user_input
        )

        if decision["should_remember"]:
            self.memory.remember(
                user_input,
                memory_type=decision[
                    "memory_type"
                ],
                importance=decision[
                    "importance"
                ],
                memory_key=decision[
                    "memory_key"
                ],
                memory_level=decision[
                    "memory_level"
                ],
            )

        self.working_memory.add(
            user_input,
            importance=5,
        )

        return response

    def _load_plugins(
        self,
        plugin_modules,
    ):
        for module_name in plugin_modules:
            self.plugins.load_module(
                module_name
            )

    def _ensure_tool_planner(self):
        if self.brain is None:
            from src.rebecca.brain import Brain

            self.brain = Brain()

        self.tool_planner = ToolPlanner(
            brain=self.brain,
            tools=self.tools,
        )

        self.tool_executor.planner = (
            self.tool_planner
        )

    def _ask_brain(self, messages):
        if self.brain is None:
            from src.rebecca.brain import Brain

            self.brain = Brain()

        return self.brain.ask(messages)
