# tool_orchestrator.py
class ToolOrchestrator:
    """Orchestrates multiple tools intelligently"""

    def __init__(self):
        self.tool_registry = {}
        self.tool_history = []

    def register_tool(self, tool_name, tool_function, description, input_schema, output_schema):
        """Register a tool with metadata"""
        self.tool_registry[tool_name] = {
            'function': tool_function,
            'description': description,
            'input': input_schema,
            'output': output_schema
        }

    def select_tool(self, task_description, context):
        """Intelligently select appropriate tool"""

        # Score each tool for the task
        tool_scores = []
        for name, tool in self.tool_registry.items():
            score = self.calculate_relevance(tool['description'], task_description)
            tool_scores.append((name, score, tool))

        # Select best tool
        tool_scores.sort(key=lambda x: x[1], reverse=True)
        best_tool = tool_scores[0] if tool_scores else None

        return best_tool

    def execute_tool_chain(self, tools_chain, initial_data):
        """Execute sequence of tools"""
        results = {}
        current_data = initial_data

        for tool_name in tools_chain:
            if tool_name in self.tool_registry:
                tool = self.tool_registry[tool_name]

                # Prepare input
                tool_input = self.prepare_input(tool['input'], current_data)

                # Execute
                result = tool['function'](**tool_input)

                # Store result
                results[tool_name] = result
                current_data.update(result)

                # Log to history
                self.tool_history.append({
                    'tool': tool_name,
                    'input': tool_input,
                    'output': result,
                    'timestamp': '...'
                })

        return results