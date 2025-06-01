from crewai import Crew, Process
from agents import create_ideation_team
from tasks import create_task_sequence, create_custom_task_sequence, ProjectRecommendationTasks
from config import config
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import traceback
import os

# Create output directory for all generated files
OUTPUT_DIR = "project_recommendation_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configure logging with output directory
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(OUTPUT_DIR, 'project_recommendation.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ProjectRecommendationCrew:
    """
    Main crew class that orchestrates the AI Project Recommendation System.
    Manages agents, tasks, and the overall workflow execution.
    """
    
    def __init__(self, additional_tools=None, custom_config=None):
        """
        Initialize the project recommendation crew.
        
        Args:
            additional_tools: Optional list of additional tools for agents
            custom_config: Optional custom configuration overrides
        """
        self.additional_tools = additional_tools or []
        self.custom_config = custom_config or {}
        self.agents = None
        self.tasks = None
        self.crew = None
        self.execution_history = []
        self.current_session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(f"Initializing ProjectRecommendationCrew - Session: {self.current_session_id}")
        logger.info(f"Output directory: {os.path.abspath(OUTPUT_DIR)}")
        
        # Initialize components
        self._initialize_agents()
        self._initialize_tasks()
        self._initialize_crew()
    
    def _initialize_agents(self):
        """Initialize all agents for the project recommendation system."""
        try:
            logger.info("Initializing agents...")
            self.agents = create_ideation_team(additional_tools=self.additional_tools)
            logger.info(f"Successfully initialized {len(self.agents)} agents")
            
            # Log agent details
            for agent_name, agent in self.agents.items():
                logger.info(f"Agent '{agent_name}' ready - Role: {agent.role}")
                
        except Exception as e:
            logger.error(f"Failed to initialize agents: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _initialize_tasks(self):
        """Initialize all tasks for the workflow."""
        try:
            logger.info("Initializing tasks...")
            self.tasks = create_task_sequence(self.agents)
            logger.info(f"Successfully initialized {len(self.tasks)} tasks")
            
            # Log task details
            for i, task in enumerate(self.tasks, 1):
                logger.info(f"Task {i}: {task.description[:100]}...")
                
        except Exception as e:
            logger.error(f"Failed to initialize tasks: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def _initialize_crew(self):
        try:
            logger.info("Initializing crew...")
            crew_config = {
                'agents': list(self.agents.values()),
                'tasks': self.tasks,
                'process': Process.sequential,
                'verbose': self.custom_config.get('verbose', True),
                'memory': False,
                'max_rpm': self.custom_config.get('max_rpm', 10),
                'max_execution_time': self.custom_config.get('max_execution_time', 1800)
            }
            self.crew = Crew(**crew_config)
            logger.info("Crew initialized successfully with memory disabled to avoid OpenAI dependency")
        except Exception as e:
            logger.error(f"Failed to initialize crew: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def run_interactive_session(self):
        print("🚀 Welcome to the AI Project Recommendation System!")
        print("=" * 60)
        print("I'll help you discover amazing projects tailored to your skills and interests.")
        print(f"📁 All files will be saved in: {os.path.abspath(OUTPUT_DIR)}")
        print("Type 'quit' or 'exit' to end the session.\n")
        try:
            while True:
                user_input = input("\n💬 You: ").strip()
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Thanks for using the AI Project Recommendation System!")
                    print(f"Your recommendations are saved in: {os.path.abspath(OUTPUT_DIR)}")
                    break
                if not user_input:
                    print("Please enter something to get started!")
                    continue
                print("\n🤖 Processing your request... This may take a few minutes.")
                results = self.run_recommendation_workflow(user_input)
                if results.get('status') == 'completed':
                    print("\n✅ Here are your personalized project recommendations!")
                    print("-" * 50)
                    print(results.get('raw_output', 'Results generated successfully!'))
                    continue_choice = input("\n❓ Would you like to refine your recommendations? (y/n): ").strip().lower()
                    if continue_choice != 'y':
                        break
                else:
                    print(f"\n❌ Sorry, something went wrong: {results.get('error', 'Unknown error')}")
                    print("Please try again with different input.")
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            logger.error(f"Interactive session error: {str(e)}")
    
    def run_recommendation_workflow(self, user_input: str = None, 
                                  save_results: bool = True) -> Dict[str, Any]:
        """
        Execute the complete project recommendation workflow.
        
        Args:
            user_input: Optional initial user input to start the conversation
            save_results: Whether to save results to files
            
        Returns:
            Dictionary containing the complete workflow results
        """
        start_time = datetime.now()
        logger.info(f"Starting project recommendation workflow - Session: {self.current_session_id}")
        
        try:
            # Prepare inputs for the crew
            inputs = {
                'session_id': self.current_session_id,
                'start_time': start_time.isoformat(),
                'user_initial_input': user_input or "Hello! I'd like to get some project recommendations."
            }
            
            # Execute the crew workflow
            logger.info("Executing crew workflow...")
            result = self.crew.kickoff(inputs=inputs)
            
            end_time = datetime.now()
            execution_duration = (end_time - start_time).total_seconds()
            
            # Process and structure the results
            processed_results = self._process_crew_results(result, execution_duration)
            
            # Save results if requested
            if save_results:
                self._save_session_results(processed_results)
            
            # Update execution history
            self.execution_history.append({
                'session_id': self.current_session_id,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'duration_seconds': execution_duration,
                'status': 'completed',
                'user_input': user_input
            })
            
            logger.info(f"Workflow completed successfully in {execution_duration:.2f} seconds")
            return processed_results
            
        except Exception as e:
            error_msg = f"Workflow execution failed: {str(e)}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            
            # Record failed execution
            self.execution_history.append({
                'session_id': self.current_session_id,
                'start_time': start_time.isoformat(),
                'end_time': datetime.now().isoformat(),
                'status': 'failed',
                'error': str(e),
                'user_input': user_input
            })
            
            return {
                'status': 'failed',
                'error': error_msg,
                'session_id': self.current_session_id
            }
    
    def _process_crew_results(self, raw_result, execution_duration: float) -> Dict[str, Any]:
        """
        Process and structure the raw crew execution results.
        
        Args:
            raw_result: Raw result from crew execution
            execution_duration: Total execution time in seconds
            
        Returns:
            Structured results dictionary
        """
        try:
            logger.info("Processing crew results...")
            
            # Extract results from different tasks/agents
            processed_results = {
                'session_id': self.current_session_id,
                'execution_summary': {
                    'status': 'completed',
                    'duration_seconds': execution_duration,
                    'timestamp': datetime.now().isoformat(),
                    'output_directory': os.path.abspath(OUTPUT_DIR)
                },
                'user_profile': {},
                'generated_projects': [],
                'ranked_projects': [],
                'final_recommendations': {},
                'raw_output': str(raw_result)
            }
            
            # Try to extract structured data from the result
            # Note: This will depend on how CrewAI returns results
            if hasattr(raw_result, 'tasks_output'):
                for i, task_output in enumerate(raw_result.tasks_output):
                    task_name = f"task_{i+1}"
                    processed_results[task_name] = {
                        'output': str(task_output),
                        'agent': task_output.agent if hasattr(task_output, 'agent') else 'unknown'
                    }
            
            # Extract key information if available
            result_str = str(raw_result).lower()
            
            # Count projects mentioned
            if 'project' in result_str:
                import re
                project_mentions = len(re.findall(r'project', result_str))
                processed_results['execution_summary']['projects_mentioned'] = project_mentions
            
            logger.info("Results processed successfully")
            return processed_results
            
        except Exception as e:
            logger.error(f"Failed to process results: {str(e)}")
            return {
                'session_id': self.current_session_id,
                'status': 'processing_failed',
                'error': str(e),
                'raw_output': str(raw_result)
            }
    
    def _save_session_results(self, results: Dict[str, Any]):
        """Save session results to files in the organized output directory."""
        try:
            # Save detailed results as JSON in the output directory
            results_filename = os.path.join(OUTPUT_DIR, f"results_{self.current_session_id}.json")
            with open(results_filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results saved to {results_filename}")
            
            # Save execution history in the output directory
            history_filename = os.path.join(OUTPUT_DIR, "execution_history.json")
            try:
                with open(history_filename, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except FileNotFoundError:
                history = []
            
            history.extend(self.execution_history)
            
            with open(history_filename, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Execution history updated in {history_filename}")
            
        except Exception as e:
            logger.error(f"Failed to save results: {str(e)}")
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get information about the current session and crew status."""
        return {
            'session_id': self.current_session_id,
            'agents_count': len(self.agents) if self.agents else 0,
            'tasks_count': len(self.tasks) if self.tasks else 0,
            'crew_initialized': self.crew is not None,
            'execution_history_count': len(self.execution_history),
            'additional_tools_count': len(self.additional_tools),
            'output_directory': os.path.abspath(OUTPUT_DIR)
        }
    
    def reset_session(self):
        """Reset the current session and generate a new session ID."""
        self.current_session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"Session reset - New session: {self.current_session_id}")

class ProjectRecommendationCrewBuilder:
    """
    Builder class for creating customized ProjectRecommendationCrew instances.
    """
    
    def __init__(self):
        self.additional_tools = []
        self.custom_config = {}
    
    def with_additional_tools(self, tools: List) -> 'ProjectRecommendationCrewBuilder':
        """Add additional tools to the crew."""
        self.additional_tools.extend(tools)
        return self
    
    def with_config(self, config: Dict[str, Any]) -> 'ProjectRecommendationCrewBuilder':
        """Add custom configuration."""
        self.custom_config.update(config)
        return self
    
    def with_verbose_mode(self, verbose: bool = True) -> 'ProjectRecommendationCrewBuilder':
        """Enable or disable verbose mode."""
        self.custom_config['verbose'] = verbose
        return self
    
    def with_memory(self, memory: bool = True) -> 'ProjectRecommendationCrewBuilder':
        """Enable or disable crew memory."""
        self.custom_config['memory'] = memory
        return self
    
    def with_hierarchical_process(self) -> 'ProjectRecommendationCrewBuilder':
        """Use hierarchical process instead of sequential."""
        self.custom_config['use_hierarchical'] = True
        return self
    
    def with_execution_timeout(self, timeout_seconds: int) -> 'ProjectRecommendationCrewBuilder':
        """Set maximum execution timeout."""
        self.custom_config['max_execution_time'] = timeout_seconds
        return self
    
    def build(self) -> ProjectRecommendationCrew:
        """Build and return the configured crew instance."""
        return ProjectRecommendationCrew(
            additional_tools=self.additional_tools,
            custom_config=self.custom_config
        )

# Convenience functions for easy usage
def create_standard_crew() -> ProjectRecommendationCrew:
    """Create a standard project recommendation crew with default settings."""
    return ProjectRecommendationCrew()

def create_verbose_crew() -> ProjectRecommendationCrew:
    """Create a crew with verbose logging enabled."""
    return (ProjectRecommendationCrewBuilder()
            .with_verbose_mode(True)
            .with_memory(True)
            .build())

def create_fast_crew() -> ProjectRecommendationCrew:
    """Create a crew optimized for faster execution."""
    return (ProjectRecommendationCrewBuilder()
            .with_verbose_mode(False)
            .with_execution_timeout(900)  # 15 minutes
            .build())

def create_hierarchical_crew() -> ProjectRecommendationCrew:
    """Create a crew using hierarchical process with a manager agent."""
    return (ProjectRecommendationCrewBuilder()
            .with_hierarchical_process()
            .with_verbose_mode(True)
            .build())

# Main execution function
def main():
    """
    Main function to run the project recommendation system.
    """
    try:
        print("🚀 Initializing AI Project Recommendation System...")
        print(f"📁 Output directory: {os.path.abspath(OUTPUT_DIR)}")
        
        # Create the crew
        crew = create_standard_crew()
        
        print(f"✅ System initialized successfully!")
        print(f"📊 Session Info: {crew.get_session_info()}")
        
        # Run interactive session
        crew.run_interactive_session()
        
    except Exception as e:
        print(f"❌ Failed to initialize system: {str(e)}")
        logger.error(f"Main execution failed: {str(e)}")
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()