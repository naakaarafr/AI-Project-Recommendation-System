import os
import sys
import json
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

# Add the current directory to the path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents import create_ideation_team
from config import config
from tools import available_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('interactive_session.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class InteractiveProjectRecommendationSystem:
    """
    Interactive system that allows real-time communication with agents.
    Agents can ask questions and receive immediate responses from the user.
    """
    
    def __init__(self):
        """Initialize the interactive system."""
        self.agents = None
        self.user_data = {}
        self.conversation_history = []
        self.current_agent = None
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize agents
        self._initialize_agents()
        
        # Welcome message
        self._show_welcome_message()
    
    def _initialize_agents(self):
        """Initialize all agents."""
        try:
            logger.info("Initializing agents...")
            self.agents = create_ideation_team()
            logger.info(f"Successfully initialized {len(self.agents)} agents")
        except Exception as e:
            logger.error(f"Failed to initialize agents: {str(e)}")
            raise
    
    def _show_welcome_message(self):
        """Display welcome message to the user."""
        print("\n" + "="*80)
        print("🚀 WELCOME TO THE AI PROJECT RECOMMENDATION SYSTEM 🚀")
        print("="*80)
        print("I'm your AI assistant team that will help you discover amazing projects")
        print("tailored to your skills, interests, and career goals!")
        print("\n📋 Here's how this works:")
        print("• I'll ask you questions about your background and interests")
        print("• You can answer naturally - just type your responses")
        print("• I'll analyze your profile and generate personalized project ideas")
        print("• Finally, I'll present you with the top 10 recommended projects")
        print("\n💡 Tips:")
        print("• Be as detailed as possible in your answers")
        print("• Type 'skip' if you want to skip a question")
        print("• Type 'back' to revisit the previous question")
        print("• Type 'quit' at any time to exit")
        print("\n" + "="*80)
        print("Let's get started! 🎯")
        print("="*80 + "\n")
    
    def ask_user(self, question: str, agent_name: str = "AI Assistant") -> str:
        """
        Ask a question to the user and get their response.
        
        Args:
            question: The question to ask
            agent_name: Name of the agent asking the question
            
        Returns:
            User's response
        """
        print(f"\n🤖 {agent_name}:")
        print("-" * 60)
        print(f"{question}")
        print("-" * 60)
        
        while True:
            try:
                response = input(f"\n💬 Your answer: ").strip()
                
                # Handle special commands
                if response.lower() == 'quit':
                    print("\n👋 Thanks for using the AI Project Recommendation System!")
                    sys.exit(0)
                elif response.lower() == 'skip':
                    response = "I'd prefer to skip this question."
                elif response.lower() == 'back':
                    print("📝 Going back to previous question...")
                    return 'BACK_COMMAND'
                elif not response:
                    print("⚠️  Please provide an answer or type 'skip' to skip this question.")
                    continue
                
                # Log the interaction
                self.conversation_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'agent': agent_name,
                    'question': question,
                    'user_response': response
                })
                
                return response
                
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"⚠️  Error getting input: {e}")
                continue
    
    def show_typing_indicator(self, message: str = "Processing your response"):
        """Show a typing indicator while processing."""
        print(f"\n⏳ {message}", end="")
        for _ in range(3):
            time.sleep(0.5)
            print(".", end="", flush=True)
        print(" ✓\n")
    
    def run_onboarding_phase(self) -> Dict[str, Any]:
        """Run the interactive onboarding phase."""
        print("\n🎯 PHASE 1: Getting to Know You")
        print("=" * 50)
        
        onboarding_agent = self.agents["User_Onboarder"]
        user_info = {}
        
        # Define the questions we need to ask
        questions = [
            {
                'key': 'name',
                'question': "What's your name? (or what would you like me to call you?)",
                'required': True
            },
            {
                'key': 'current_role',
                'question': "What's your current role or status? (e.g., student, software developer, career changer, etc.)",
                'required': True
            },
            {
                'key': 'experience_level',
                'question': "How would you describe your overall experience with programming/technology? (beginner, intermediate, advanced, expert)",
                'required': True
            },
            {
                'key': 'programming_languages',
                'question': "Which programming languages do you know? Please list them with your comfort level (e.g., 'Python - intermediate, JavaScript - beginner')",
                'required': True
            },
            {
                'key': 'interests',
                'question': "What areas of technology interest you most? (e.g., AI/ML, Web Development, Mobile Apps, Data Science, Game Development, etc.)",
                'required': True
            },
            {
                'key': 'career_goals',
                'question': "What are your career goals? What do you hope to achieve in the next 6-12 months?",
                'required': True
            },
            {
                'key': 'time_commitment',
                'question': "How much time can you dedicate to a project per week? (e.g., 2-3 hours, 5-10 hours, 15+ hours)",
                'required': True
            },
            {
                'key': 'project_preferences',
                'question': "What type of projects appeal to you? (learning projects, portfolio pieces, potential business ideas, open source contributions, etc.)",
                'required': False
            },
            {
                'key': 'technologies_to_learn',
                'question': "Are there any specific technologies or frameworks you're excited to learn?",
                'required': False
            },
            {
                'key': 'budget_constraints',
                'question': "Do you have any budget constraints for tools, hosting, or resources? (free only, low budget, moderate budget, no constraints)",
                'required': False
            }
        ]
        
        question_index = 0
        while question_index < len(questions):
            q = questions[question_index]
            
            response = self.ask_user(q['question'], "Ava (User Onboarder)")
            
            if response == 'BACK_COMMAND' and question_index > 0:
                question_index -= 1
                continue
            elif response == 'BACK_COMMAND':
                print("📝 You're already at the first question!")
                continue
            
            user_info[q['key']] = response
            question_index += 1
        
        # Show summary of collected information
        self.show_typing_indicator("Analyzing your responses")
        self._show_user_summary(user_info)
        
        return user_info
    
    def _show_user_summary(self, user_info: Dict[str, Any]):
        """Show a summary of the collected user information."""
        print("\n📊 PROFILE SUMMARY")
        print("=" * 50)
        print(f"👤 Name: {user_info.get('name', 'N/A')}")
        print(f"💼 Role: {user_info.get('current_role', 'N/A')}")
        print(f"⭐ Experience: {user_info.get('experience_level', 'N/A')}")
        print(f"💻 Languages: {user_info.get('programming_languages', 'N/A')}")
        print(f"🎯 Interests: {user_info.get('interests', 'N/A')}")
        print(f"🚀 Goals: {user_info.get('career_goals', 'N/A')}")
        print(f"⏰ Time Available: {user_info.get('time_commitment', 'N/A')}")
        print("=" * 50)
        
        confirm = input("\n✅ Does this look correct? (y/n): ").strip().lower()
        if confirm != 'y':
            print("📝 Let's go back and update your information...")
            return False
        return True
    
    def run_profile_analysis_phase(self, user_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the user profile and create structured data."""
        print("\n🔍 PHASE 2: Analyzing Your Profile")
        print("=" * 50)
        
        self.show_typing_indicator("Analyzing your skills and background")
        
        # Create structured profile
        profile = {
            'profile_id': self.session_id,
            'created_at': datetime.now().isoformat(),
            'personal_info': {
                'name': user_info.get('name', ''),
                'current_role': user_info.get('current_role', ''),
                'experience_level': self._standardize_experience_level(user_info.get('experience_level', ''))
            },
            'technical_profile': {
                'programming_languages': self._parse_languages(user_info.get('programming_languages', '')),
                'preferred_technologies': user_info.get('technologies_to_learn', '').split(',') if user_info.get('technologies_to_learn') else []
            },
            'interests_and_goals': {
                'domains': user_info.get('interests', '').split(',') if user_info.get('interests') else [],
                'career_goals': user_info.get('career_goals', ''),
                'project_preferences': user_info.get('project_preferences', '')
            },
            'constraints': {
                'time_commitment': user_info.get('time_commitment', ''),
                'budget_range': user_info.get('budget_constraints', 'free')
            }
        }
        
        print("✅ Profile analysis complete!")
        print(f"📈 Detected {len(profile['technical_profile']['programming_languages'])} programming languages")
        print(f"🎯 Identified {len(profile['interests_and_goals']['domains'])} areas of interest")
        
        return profile
    
    def _standardize_experience_level(self, experience: str) -> str:
        """Standardize experience level."""
        experience = experience.lower().strip()
        if any(word in experience for word in ['beginner', 'new', 'start', 'learning']):
            return 'beginner'
        elif any(word in experience for word in ['intermediate', 'some', 'moderate']):
            return 'intermediate'
        elif any(word in experience for word in ['advanced', 'experienced', 'senior']):
            return 'advanced'
        elif any(word in experience for word in ['expert', 'professional', 'master']):
            return 'expert'
        return experience
    
    def _parse_languages(self, languages_str: str) -> List[Dict[str, str]]:
        """Parse programming languages from string."""
        languages = []
        if not languages_str:
            return languages
        
        # Simple parsing - split by comma and try to extract language and level
        parts = languages_str.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                lang, level = part.split('-', 1)
                languages.append({'language': lang.strip(), 'level': level.strip()})
            else:
                languages.append({'language': part, 'level': 'unknown'})
        
        return languages
    
    def run_project_generation_phase(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate project ideas based on user profile."""
        print("\n💡 PHASE 3: Generating Project Ideas")
        print("=" * 50)
        
        self.show_typing_indicator("Researching trending technologies and generating ideas")
        
        # Simulate project generation based on profile
        projects = self._generate_sample_projects(profile)
        
        print(f"✅ Generated {len(projects)} unique project ideas!")
        print("🔍 Projects span multiple domains and difficulty levels")
        
        return projects
    
    def _generate_sample_projects(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate sample projects based on user profile."""
        # This is a simplified version - in the real system, this would use the AI agents
        
        experience_level = profile['personal_info']['experience_level']
        interests = profile['interests_and_goals']['domains']
        languages = [lang['language'] for lang in profile['technical_profile']['programming_languages']]
        
        # Sample project templates
        project_templates = [
            {
                'title': 'Personal Finance Tracker',
                'description': 'Build a web application to track income, expenses, and savings goals with data visualization.',
                'domain': 'Web Development',
                'technologies': ['Python', 'Flask', 'SQLite', 'Chart.js'],
                'difficulty': 'intermediate',
                'estimated_time': '3-4 weeks'
            },
            {
                'title': 'AI-Powered Recipe Recommender',
                'description': 'Create a machine learning system that recommends recipes based on dietary preferences and available ingredients.',
                'domain': 'AI/ML',
                'technologies': ['Python', 'scikit-learn', 'pandas', 'Flask'],
                'difficulty': 'intermediate',
                'estimated_time': '4-6 weeks'
            },
            {
                'title': 'Weather Dashboard with API Integration',
                'description': 'Build a responsive dashboard that displays weather data from multiple sources with interactive maps.',
                'domain': 'Web Development',
                'technologies': ['JavaScript', 'React', 'APIs', 'CSS'],
                'difficulty': 'beginner',
                'estimated_time': '2-3 weeks'
            },
            {
                'title': 'Task Management System',
                'description': 'Develop a full-stack application for managing projects and tasks with team collaboration features.',
                'domain': 'Full Stack',
                'technologies': ['Node.js', 'Express', 'MongoDB', 'React'],
                'difficulty': 'intermediate',
                'estimated_time': '5-7 weeks'
            },
            {
                'title': 'Stock Price Predictor',
                'description': 'Build an ML model to predict stock prices using historical data and market indicators.',
                'domain': 'Data Science',
                'technologies': ['Python', 'TensorFlow', 'pandas', 'matplotlib'],
                'difficulty': 'advanced',
                'estimated_time': '6-8 weeks'
            }
        ]
        
        # Filter and customize projects based on user profile
        filtered_projects = []
        for template in project_templates:
            # Adjust difficulty based on user experience
            if experience_level == 'beginner' and template['difficulty'] == 'advanced':
                continue
            elif experience_level == 'expert' and template['difficulty'] == 'beginner':
                template['difficulty'] = 'intermediate'
            
            # Add personalization based on interests
            template['relevance_score'] = self._calculate_relevance(template, interests, languages)
            template['learning_outcomes'] = self._generate_learning_outcomes(template)
            template['portfolio_value'] = 'High' if template['relevance_score'] > 0.7 else 'Medium'
            
            filtered_projects.append(template)
        
        # Sort by relevance and return top projects
        filtered_projects.sort(key=lambda x: x['relevance_score'], reverse=True)
        return filtered_projects[:10]
    
    def _calculate_relevance(self, project: Dict, interests: List[str], languages: List[str]) -> float:
        """Calculate relevance score for a project."""
        score = 0.5  # Base score
        
        # Check domain alignment
        project_domain = project['domain'].lower()
        for interest in interests:
            if interest.lower().strip() in project_domain:
                score += 0.3
        
        # Check technology alignment
        project_techs = [tech.lower() for tech in project['technologies']]
        for lang in languages:
            if lang.lower() in project_techs:
                score += 0.2
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _generate_learning_outcomes(self, project: Dict) -> List[str]:
        """Generate learning outcomes for a project."""
        outcomes = []
        for tech in project['technologies'][:3]:  # Top 3 technologies
            outcomes.append(f"Hands-on experience with {tech}")
        
        outcomes.append(f"{project['domain']} project architecture")
        outcomes.append("Project planning and execution")
        
        return outcomes
    
    def run_project_ranking_phase(self, projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank and filter the generated projects."""
        print("\n🏆 PHASE 4: Ranking Projects")
        print("=" * 50)
        
        self.show_typing_indicator("Scoring projects based on relevance, feasibility, and impact")
        
        # Add ranking scores to projects
        for i, project in enumerate(projects):
            project['rank'] = i + 1
            project['overall_score'] = round(project.get('relevance_score', 0.5) * 10, 1)
            project['feasibility_score'] = 8.5  # Simplified
            project['impact_score'] = 8.0  # Simplified
        
        print(f"✅ Ranked {len(projects)} projects successfully!")
        print("📊 Applied multi-dimensional scoring algorithm")
        
        return projects[:5]  # Return top 5
    
    def run_presentation_phase(self, ranked_projects: List[Dict[str, Any]], profile: Dict[str, Any]) -> Dict[str, Any]:
        """Present the final recommendations to the user."""
        print("\n🎉 PHASE 5: Your Personalized Project Recommendations")
        print("=" * 70)
        
        user_name = profile['personal_info']['name']
        experience = profile['personal_info']['experience_level']
        
        print(f"\n👋 Hey {user_name}!")
        print(f"Based on your {experience}-level background and interests, here are your")
        print("top project recommendations that will help you grow and build an impressive portfolio:\n")
        
        for i, project in enumerate(ranked_projects, 1):
            print(f"🏆 RANK #{i}: {project['title']}")
            print("-" * 50)
            print(f"📝 Description: {project['description']}")
            print(f"🛠️  Technologies: {', '.join(project['technologies'])}")
            print(f"📊 Difficulty: {project['difficulty'].title()}")
            print(f"⏱️  Estimated Time: {project['estimated_time']}")
            print(f"⭐ Overall Score: {project['overall_score']}/10")
            print(f"💼 Portfolio Value: {project.get('portfolio_value', 'High')}")
            
            if project.get('learning_outcomes'):
                print(f"🎯 What You'll Learn:")
                for outcome in project['learning_outcomes'][:3]:
                    print(f"   • {outcome}")
            
            print()
        
        # Save recommendations
        self._save_recommendations(ranked_projects, profile)
        
        # Ask for feedback
        self._get_user_feedback()
        
        return {
            'recommendations': ranked_projects,
            'user_profile': profile,
            'session_id': self.session_id
        }
    
    def _save_recommendations(self, projects: List[Dict[str, Any]], profile: Dict[str, Any]):
        """Save recommendations to files."""
        try:
            # Save as JSON
            results = {
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat(),
                'user_profile': profile,
                'recommendations': projects,
                'conversation_history': self.conversation_history
            }
            
            filename = f"recommendations_{self.session_id}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Your recommendations have been saved to '{filename}'")
            
        except Exception as e:
            logger.error(f"Failed to save recommendations: {e}")
            print("⚠️  Could not save recommendations to file, but they're displayed above!")
    
    def _get_user_feedback(self):
        """Get feedback from the user."""
        print("\n📋 FEEDBACK")
        print("=" * 30)
        
        feedback_questions = [
            "How satisfied are you with these recommendations? (1-10)",
            "Which project interests you most?",
            "Is there anything specific you'd like to see in future recommendations?"
        ]
        
        feedback = {}
        for question in feedback_questions:
            try:
                response = input(f"❓ {question}\n💬 Your answer: ").strip()
                if response:
                    feedback[question] = response
            except KeyboardInterrupt:
                break
        
        if feedback:
            print("\n🙏 Thank you for your feedback!")
            
            # Save feedback
            try:
                feedback_file = f"feedback_{self.session_id}.json"
                with open(feedback_file, 'w', encoding='utf-8') as f:
                    json.dump(feedback, f, indent=2)
            except Exception as e:
                logger.error(f"Failed to save feedback: {e}")
    
    def run_complete_workflow(self):
        """Run the complete interactive workflow."""
        try:
            # Phase 1: Onboarding
            user_info = self.run_onboarding_phase()
            
            # Phase 2: Profile Analysis
            profile = self.run_profile_analysis_phase(user_info)
            
            # Phase 3: Project Generation
            projects = self.run_project_generation_phase(profile)
            
            # Phase 4: Project Ranking
            ranked_projects = self.run_project_ranking_phase(projects)
            
            # Phase 5: Presentation
            final_results = self.run_presentation_phase(ranked_projects, profile)
            
            # Completion message
            print("\n" + "="*70)
            print("🎯 WORKFLOW COMPLETE!")
            print("="*70)
            print("Your personalized project recommendations are ready!")
            print("📁 Check the generated files for detailed information.")
            print("🚀 Happy coding, and good luck with your projects!")
            print("="*70)
            
            return final_results
            
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted by user. Goodbye!")
            return None
        except Exception as e:
            logger.error(f"Workflow failed: {e}")
            print(f"\n❌ An error occurred: {e}")
            print("Please try running the system again.")
            return None

def main():
    """Main function to run the interactive system."""
    try:
        # Create and run the interactive system
        system = InteractiveProjectRecommendationSystem()
        results = system.run_complete_workflow()
        
        if results:
            print(f"\n📊 Session completed successfully!")
            print(f"Session ID: {results['session_id']}")
        
    except Exception as e:
        print(f"❌ Failed to start the system: {e}")
        logger.error(f"System startup failed: {e}")

if __name__ == "__main__":
    main()