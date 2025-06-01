from crewai import Task
from typing import Dict, Any, List
import json

class ProjectRecommendationTasks:
    """
    Task definitions for the AI Project Recommendation System.
    Each task corresponds to a specific agent's responsibility in the workflow.
    """

    def __init__(self):
        """Initialize task definitions."""
        pass

    def create_user_onboarding_task(self, agent) -> Task:
        """
        Task for collecting comprehensive user information through natural conversation.
        """
        return Task(
            description="""            
            Conduct a comprehensive yet natural onboarding conversation with the user to gather all necessary information for project recommendations. You must collect:

            **Required Information:**
            1. Personal Details:
            - Name and preferred way to be addressed
            - Current role/position (student, professional, career changer, etc.)
            - Years of experience in tech/programming

            2. Technical Background:
            - Programming languages known (with proficiency levels)
            - Frameworks, libraries, and tools experience
            - Previous projects or notable work
            - Preferred development environment

            3. Interests & Goals:
            - Domains of interest (AI/ML, Web Dev, Mobile, Data Science, etc.)
            - Short-term and long-term career goals
            - Specific technologies they want to learn
            - Industry sectors they're passionate about

            4. Constraints & Preferences:
            - Available time commitment (hours per week)
            - Budget constraints for tools/resources
            - Preference for solo vs collaborative projects
            - Timeline expectations for project completion

            **Conversation Guidelines:**
            - Start with a warm, welcoming tone
            - Ask follow-up questions to clarify ambiguous responses
            - Adapt questioning style based on user engagement
            - Use examples to help users articulate their interests
            - Validate information by summarizing key points
            - Ensure privacy and explain how data will be used

            **Expected Output:**
            A comprehensive dictionary containing all collected user information, structured for easy processing by downstream agents.
            """,
            agent=agent,
            expected_output="""            
            A detailed user information dictionary with the following structure:
            {
                "name": "User's name",
                "experience_level": "beginner/intermediate/advanced/expert",
                "career_stage": "student/professional/career_changer/freelancer",
                "skills": ["list", "of", "technical", "skills"],
                "programming_languages": ["Python", "JavaScript", "etc"],
                "preferred_technologies": ["React", "Django", "etc"],
                "interests": ["AI/ML", "Web Development", "etc"],
                "career_goals": ["Short term goals", "Long term goals"],
                "time_commitment": "low/moderate/high (hours per week)",
                "budget_range": "free/low/moderate/high",
                "collaboration_preference": "solo/team/either",
                "project_preferences": {
                    "complexity": "simple/moderate/complex",
                    "duration": "short/medium/long",
                    "type": "learning/portfolio/commercial"
                },
                "additional_context": "Any other relevant information"
            }
            """,
            human_input=True  # Enable pausing for user input
        )

    def create_profile_analysis_task(self, agent) -> Task:
        """
        Task for analyzing and structuring user data into a machine-readable profile.
        """
        return Task(
            description="""
            Analyze the raw user information collected during onboarding and create a structured, validated user profile. Your responsibilities include:

            **Data Validation & Cleaning:**
            1. Validate all user inputs for consistency and completeness
            2. Flag any contradictions (e.g., "10 years experience" but "beginner" level)
            3. Standardize skill names and experience levels
            4. Extract implicit skills from project descriptions
            5. Cross-reference stated skills with mentioned projects

            **Profile Structuring:**
            1. Create a comprehensive JSON profile using the create_user_profile_json tool
            2. Calculate profile completeness score
            3. Identify missing critical information
            4. Suggest areas for clarification if needed

            **Contradiction Resolution:**
            1. Identify inconsistencies in user responses
            2. Provide specific questions to resolve ambiguities
            3. Flag confidence levels for different profile sections
            4. Recommend follow-up questions for unclear areas

            **Quality Assurance:**
            1. Ensure all required fields are populated
            2. Validate experience levels against stated skills
            3. Check logical consistency in goals and constraints
            4. Prepare profile for optimal project matching

            Use the available tools: validate_user_input, extract_skills_from_text, and create_user_profile_json.
            """,
            agent=agent,
            expected_output="""
            A structured JSON user profile with validation results:
            {{
                "profile": {{
                    "profile_id": "unique_identifier",
                    "created_at": "timestamp",
                    "personal_info": {{}},
                    "technical_profile": {{}},
                    "interests_and_goals": {{}},
                    "constraints": {{}},
                    "metadata": {{
                        "profile_completeness": 0.85,
                        "confidence_score": 0.9,
                        "validation_status": "validated"
                    }}
                }},
                "validation_results": {{
                    "is_valid": true,
                    "errors": [],
                    "warnings": ["Any warnings about unclear information"],
                    "suggestions": ["Recommendations for profile improvement"]
                }},
                "extracted_skills": ["Additional", "skills", "found", "in", "text"],
                "confidence_flags": {{
                    "experience_level": "high",
                    "skill_assessment": "medium",
                    "goal_clarity": "high"
                }}
            }}
            """
        )

    def create_project_generation_task(self, agent) -> Task:
        """
        Task for generating diverse, industry-relevant project ideas.
        """
        return Task(
            description="""
            Generate 20-30 innovative, industry-relevant project ideas tailored to the user's profile. Your mission is to create diverse, executable projects that span multiple domains and difficulty levels.

            **Project Generation Strategy:**
            1. **Industry Trend Integration:**
               - Use search_github_trending to find current popular technologies
               - Use search_tech_news to identify emerging trends and opportunities
               - Cross-reference trending topics with user interests

            2. **Diversity Requirements:**
               - Generate projects across multiple domains (AI/ML, Web, Mobile, Data Science, etc.)
               - Include various difficulty levels appropriate for user's experience
               - Mix different project types: learning projects, portfolio pieces, potential commercial ventures
               - Ensure technology diversity while respecting user preferences

            3. **Personalization Factors:**
               - Align with user's stated interests and career goals
               - Consider user's current skill level and desired growth areas
               - Respect time and budget constraints
               - Factor in collaboration preferences

            4. **Industry Relevance:**
               - Focus on projects that demonstrate real-world applications
               - Include projects that solve actual problems in user's domains of interest
               - Ensure projects showcase skills relevant to current job market
               - Consider scalability and potential for portfolio enhancement

            5. **Project Specifications:**
               - Each project should have clear deliverables
               - Include specific technology stacks
               - Provide realistic time estimates
               - Assess potential impact and learning outcomes

            Use tools: search_github_trending, search_tech_news, and generate_project_ideas.
            """,
            agent=agent,
            expected_output="""
            A comprehensive list of 20-30 project ideas with detailed specifications:
            [
                {{
                    "title": "Project Title",
                    "description": "Detailed project description with clear objectives",
                    "domain": "AI/ML, Web Development, etc.",
                    "difficulty": "beginner/intermediate/advanced",
                    "technologies": ["Required", "technologies", "and", "tools"],
                    "estimated_time": "Realistic time estimate",
                    "learning_outcomes": ["Skills", "user", "will", "gain"],
                    "deliverables": ["Specific", "project", "outputs"],
                    "industry_relevance": "Why this project matters in current market",
                    "scalability_potential": "How project can be expanded",
                    "portfolio_value": "How this enhances user's portfolio",
                    "complexity_breakdown": {{
                        "backend": "complexity level",
                        "frontend": "complexity level",
                        "deployment": "complexity level"
                    }},
                    "inspiration_source": "GitHub trending/News article/Industry need",
                    "target_audience": "Who would use this project",
                    "impact_score": 8.5
                }}
            ]
            """
        )

    def create_project_ranking_task(self, agent) -> Task:
        """
        Task for ranking and filtering projects using sophisticated scoring algorithms.
        """
        return Task(
            description="""
            Apply rigorous ranking algorithms to prioritize the generated projects using a multi-dimensional scoring system. Your role is to be the quality gatekeeper, ensuring only the most suitable projects reach the user.

            **Ranking Methodology:**

            1. **Three-Axis Scoring System:**
               - **Relevance Score (40% weight):** How well the project aligns with user's interests, goals, and current skill level
               - **Feasibility Score (30% weight):** How realistic the project is given user's constraints (time, experience, resources)
               - **Impact Score (30% weight):** Potential value for user's career, learning, and portfolio development

            2. **Scoring Criteria:**

               **Relevance Factors:**
               - Alignment with stated interests and career goals
               - Match with current skill level and desired growth areas
               - Technology stack compatibility with user preferences
               - Domain expertise overlap

               **Feasibility Factors:**
               - Time commitment vs. user availability
               - Technical complexity vs. user experience level
               - Resource requirements vs. user constraints
               - Learning curve steepness

               **Impact Factors:**
               - Portfolio enhancement potential
               - Industry demand for demonstrated skills
               - Networking and collaboration opportunities
               - Career advancement potential

            3. **Quality Assurance:**
               - Eliminate redundant or overly similar projects
               - Ensure diversity in final selection (no more than 2 projects per domain)
               - Verify each project has unique value proposition
               - Remove projects with unrealistic requirements

            4. **Final Selection:**
               - Rank all projects by composite score
               - Apply diversity filters to ensure variety
               - Select top 10 projects with detailed justification
               - Provide scoring breakdown for transparency

            Use the rank_projects tool for systematic evaluation.
            """,
            agent=agent,
            expected_output="""
            Top 10 ranked projects with comprehensive scoring and justification:
            [
                {{
                    "rank": 1,
                    "title": "Project Title",
                    "description": "Project description",
                    "technologies": ["Tech", "stack"],
                    "difficulty": "Level",
                    "estimated_time": "Time estimate",
                    "overall_score": 8.7,
                    "relevance_score": 9.2,
                    "feasibility_score": 8.5,
                    "impact_score": 8.4,
                    "scoring_breakdown": {{
                        "relevance_factors": {{
                            "interest_alignment": 9.0,
                            "skill_match": 8.5,
                            "goal_alignment": 9.5
                        }},
                        "feasibility_factors": {{
                            "time_realistic": 8.0,
                            "complexity_appropriate": 9.0,
                            "resource_available": 8.5
                        }},
                        "impact_factors": {{
                            "portfolio_value": 9.0,
                            "industry_demand": 8.0,
                            "learning_potential": 8.2
                        }}
                    }},
                    "selection_rationale": "Why this project was selected and ranked at this position",
                    "unique_value_proposition": "What makes this project special",
                    "diversity_category": "AI/ML Project"
                }}
            ]
            """
        )

    def create_presentation_task(self, agent) -> Task:
        """
        Task for creating compelling presentations of the final project recommendations.
        """
        return Task(
            description="""
            Transform the ranked project recommendations into compelling, actionable presentations that inspire and guide the user toward their next great project. Your role is to be the storyteller who makes technical projects feel exciting and achievable.

            **Presentation Objectives:**
            1. **Narrative Crafting:**
               - Create engaging stories around each project
               - Highlight unique value propositions and potential impact
               - Frame projects as exciting opportunities rather than just tasks
               - Connect projects to user's personal journey and goals

            2. **Practical Guidance:**
               - Provide clear next steps for each project
               - Include specific resource recommendations
               - Suggest learning paths for required technologies
               - Offer tips for successful project execution

            3. **Motivation & Inspiration:**
               - Emphasize the career benefits of each project
               - Share success stories or examples of similar projects
               - Highlight portfolio enhancement opportunities
               - Connect projects to industry trends and demands

            4. **Personalization:**
               - Reference user's specific interests and goals
               - Acknowledge their current skill level and growth trajectory
               - Customize advice based on their constraints and preferences
               - Make recommendations feel tailored and thoughtful

            5. **Actionable Formats:**
               - Create multiple presentation formats (detailed overview, quick reference, CSV export)
               - Include priority recommendations
               - Provide implementation roadmaps
               - Offer alternatives and variations

            **Presentation Formats to Create:**
            1. Detailed narrative presentation with project stories
            2. Quick reference guide for easy browsing
            3. CSV export for offline analysis
            4. Implementation roadmap with suggested order

            Use tools: format_project_presentation, save_project_recommendations, and export_to_csv.
            """,
            agent=agent,
            expected_output="""
            A comprehensive presentation package including:

            1. **Executive Summary:**
               "Based on your profile as a [user description], here are 10 industry-level projects that will accelerate your journey toward [user goals]. These projects were selected from 30+ candidates and scored based on relevance, feasibility, and career impact."

            2. **Detailed Project Presentations:**
               For each of the top 10 projects:
               - Compelling project narrative with real-world context
               - Clear value proposition and career benefits
               - Specific technical requirements and learning path
               - Implementation roadmap with milestones
               - Success metrics and portfolio positioning
               - Resource recommendations and next steps

            3. **Quick Reference Guide:**
               - One-page summary of all 10 projects
               - Key technologies and time commitments
               - Difficulty levels and prerequisites
               - Priority recommendations

            4. **Implementation Strategy:**
               - Suggested project order based on learning progression
               - Skill development pathway
               - Timeline recommendations
               - Tips for success and common pitfalls to avoid

            5. **Additional Resources:**
               - Links to relevant learning materials
               - Community resources and support groups
               - Tool recommendations and setup guides
               - Portfolio presentation strategies

            6. **Export Files:**
               - JSON file with complete project data
               - CSV file for spreadsheet analysis
               - Markdown file for documentation
            """
        )

    def create_workflow_coordination_task(self, agent=None) -> Task:
        """
        Optional task for coordinating the entire workflow across all agents.
        """
        return Task(
            description="""
            Coordinate the entire project recommendation workflow, ensuring smooth handoffs between agents and maintaining context throughout the process.

            **Workflow Coordination:**
            1. Monitor progress of each task
            2. Ensure data consistency between agent handoffs
            3. Handle error recovery and fallback scenarios
            4. Validate that each agent's output meets quality standards
            5. Coordinate timing and dependencies between tasks
            6. Maintain user context throughout the entire process

            **Quality Assurance:**
            1. Verify that user profile is complete before project generation
            2. Ensure project ideas meet diversity and quality requirements
            3. Validate that ranking algorithm produces sensible results
            4. Confirm final presentations are personalized and actionable

            **Error Handling:**
            1. Identify and resolve data inconsistencies
            2. Handle missing or incomplete information
            3. Provide fallback options when tools fail
            4. Ensure graceful degradation of service quality
            """,
            agent=agent,
            expected_output="""
            Workflow coordination report:
            {{
                "workflow_status": "completed/failed/in_progress",
                "task_completion": {{
                    "onboarding": "success/failed",
                    "profile_analysis": "success/failed", 
                    "project_generation": "success/failed",
                    "project_ranking": "success/failed",
                    "presentation": "success/failed"
                }},
                "quality_metrics": {{
                    "profile_completeness": 0.85,
                    "project_diversity": 0.90,
                    "ranking_consistency": 0.88,
                    "presentation_quality": 0.92
                }},
                "error_log": ["Any", "errors", "encountered"],
                "recommendations": ["Suggestions", "for", "improvement"],
                "user_satisfaction_prediction": 0.89
            }}
            """
        )

def create_task_sequence(agents: Dict[str, Any]) -> List[Task]:
    """
    Create the complete sequence of tasks for the project recommendation system.
    
    Args:
        agents: Dictionary containing all agent instances
    
    Returns:
        List of tasks in execution order
    """
    task_factory = ProjectRecommendationTasks()
    
    # Create tasks in dependency order
    tasks = [
        task_factory.create_user_onboarding_task(agents["User_Onboarder"]),
        task_factory.create_profile_analysis_task(agents["User_Profile_Analyst"]),
        task_factory.create_project_generation_task(agents["Project_Generator"]),
        task_factory.create_project_ranking_task(agents["Project_Ranker"]),
        task_factory.create_presentation_task(agents["Presentation_Specialist"])
    ]
    
    return tasks

def create_custom_task_sequence(agents: Dict[str, Any], user_requirements: Dict[str, Any] = None) -> List[Task]:
    """
    Create a customized task sequence based on specific user requirements.
    
    Args:
        agents: Dictionary containing all agent instances
        user_requirements: Optional dictionary with custom requirements
    
    Returns:
        List of customized tasks
    """
    task_factory = ProjectRecommendationTasks()
    tasks = []
    
    # Always include core tasks
    tasks.extend([
        task_factory.create_user_onboarding_task(agents["User_Onboarder"]),
        task_factory.create_profile_analysis_task(agents["User_Profile_Analyst"]),
        task_factory.create_project_generation_task(agents["Project_Generator"]),
        task_factory.create_project_ranking_task(agents["Project_Ranker"]),
        task_factory.create_presentation_task(agents["Presentation_Specialist"])
    ])
    
    # Add workflow coordination if requested
    if user_requirements and user_requirements.get("include_coordination", False):
        coordination_task = task_factory.create_workflow_coordination_task()
        tasks.append(coordination_task)
    
    return tasks