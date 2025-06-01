import requests
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import time
import random
from crewai_tools import tool
import os
from urllib.parse import urljoin, urlparse
import csv
from io import StringIO

# =============================================================================
# WEB SCRAPING AND DATA COLLECTION TOOLS
# =============================================================================

@tool
def search_github_trending(language: str = "", time_range: str = "daily") -> Dict[str, Any]:
    """
    Search GitHub trending repositories for project inspiration.
    
    Args:
        language: Programming language filter (e.g., 'python', 'javascript')
        time_range: Time range for trending ('daily', 'weekly', 'monthly')
    
    Returns:
        Dictionary containing trending repositories data
    """
    try:
        # GitHub trending API endpoint (unofficial)
        base_url = "https://api.github.com/search/repositories"
        
        # Calculate date for trending search
        if time_range == "daily":
            date_filter = "created:>2024-01-01"
        elif time_range == "weekly":
            date_filter = "created:>2023-12-01"
        else:
            date_filter = "created:>2023-01-01"
        
        # Build query
        query = f"stars:>100 {date_filter}"
        if language:
            query += f" language:{language}"
        
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": 20
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            trending_repos = []
            for repo in data.get('items', [])[:10]:
                trending_repos.append({
                    'name': repo['name'],
                    'description': repo.get('description', ''),
                    'language': repo.get('language', ''),
                    'stars': repo['stargazers_count'],
                    'url': repo['html_url'],
                    'topics': repo.get('topics', [])
                })
            
            return {
                'success': True,
                'data': trending_repos,
                'total_count': len(trending_repos)
            }
        else:
            return {'success': False, 'error': f'API request failed: {response.status_code}'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

@tool
def search_tech_news(query: str = "AI trends") -> Dict[str, Any]:
    """
    Search for latest technology news and trends.
    
    Args:
        query: Search query for tech news
    
    Returns:
        Dictionary containing news articles
    """
    try:
        # Using a simple news API approach
        # Note: In production, you'd use NewsAPI or similar service
        
        # Simulate tech news data (replace with actual API in production)
        tech_trends = [
            {
                'title': 'AI Agents Revolutionizing Software Development',
                'summary': 'Multi-agent systems are becoming mainstream in enterprise applications',
                'category': 'AI/ML',
                'relevance_score': 0.9
            },
            {
                'title': 'Edge Computing Integration with IoT Devices',
                'summary': 'Real-time processing capabilities driving new project opportunities',
                'category': 'IoT/Edge',
                'relevance_score': 0.8
            },
            {
                'title': 'Sustainable Tech Solutions in High Demand',
                'summary': 'Green technology projects receiving increased funding',
                'category': 'Sustainability',
                'relevance_score': 0.85
            }
        ]
        
        # Filter based on query
        filtered_trends = []
        query_lower = query.lower()
        for trend in tech_trends:
            if any(keyword in trend['title'].lower() or keyword in trend['summary'].lower() 
                   for keyword in query_lower.split()):
                filtered_trends.append(trend)
        
        return {
            'success': True,
            'data': filtered_trends,
            'search_query': query
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

# =============================================================================
# USER PROFILE AND DATA PROCESSING TOOLS
# =============================================================================

@tool
def validate_user_input(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and clean user input data for profile creation.
    
    Args:
        input_data: Raw user input dictionary
    
    Returns:
        Dictionary with validation results and cleaned data
    """
    try:
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'cleaned_data': {},
            'confidence_score': 1.0
        }
        
        # Define validation rules
        required_fields = ['name', 'experience_level', 'interests']
        optional_fields = ['skills', 'preferred_technologies', 'career_goals', 'time_commitment']
        
        # Check required fields
        for field in required_fields:
            if field not in input_data or not input_data[field]:
                validation_results['errors'].append(f"Missing required field: {field}")
                validation_results['is_valid'] = False
        
        # Clean and validate data
        for key, value in input_data.items():
            if isinstance(value, str):
                # Clean string data
                cleaned_value = value.strip()
                if cleaned_value:
                    validation_results['cleaned_data'][key] = cleaned_value
            elif isinstance(value, list):
                # Clean list data
                cleaned_list = [item.strip() for item in value if isinstance(item, str) and item.strip()]
                if cleaned_list:
                    validation_results['cleaned_data'][key] = cleaned_list
            else:
                validation_results['cleaned_data'][key] = value
        
        # Experience level validation
        if 'experience_level' in validation_results['cleaned_data']:
            exp_level = validation_results['cleaned_data']['experience_level'].lower()
            valid_levels = ['beginner', 'intermediate', 'advanced', 'expert']
            if exp_level not in valid_levels:
                validation_results['warnings'].append(f"Experience level '{exp_level}' may need clarification")
                validation_results['confidence_score'] -= 0.1
        
        # Calculate overall confidence
        if validation_results['errors']:
            validation_results['confidence_score'] = 0.0
        elif validation_results['warnings']:
            validation_results['confidence_score'] -= len(validation_results['warnings']) * 0.1
        
        return validation_results
        
    except Exception as e:
        return {
            'is_valid': False,
            'errors': [str(e)],
            'warnings': [],
            'cleaned_data': {},
            'confidence_score': 0.0
        }

@tool
def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract technical skills and technologies from user text.
    
    Args:
        text: Input text containing skill descriptions
    
    Returns:
        List of extracted skills
    """
    try:
        # Common tech skills and frameworks (expandable)
        skill_patterns = {
            'programming_languages': [
                'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift',
                'kotlin', 'typescript', 'r', 'scala', 'perl', 'dart', 'matlab'
            ],
            'frameworks': [
                'react', 'angular', 'vue', 'django', 'flask', 'express', 'spring', 'laravel',
                'tensorflow', 'pytorch', 'keras', 'fastapi', 'nextjs', 'nuxt'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'sqlite', 'oracle',
                'dynamodb', 'cassandra', 'neo4j'
            ],
            'cloud_tools': [
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'gitlab',
                'circleci', 'ansible'
            ],
            'data_science': [
                'pandas', 'numpy', 'matplotlib', 'seaborn', 'jupyter', 'tableau', 'power bi',
                'apache spark', 'hadoop', 'airflow'
            ]
        }
        
        extracted_skills = []
        text_lower = text.lower()
        
        # Extract skills using pattern matching
        for category, skills in skill_patterns.items():
            for skill in skills:
                if skill in text_lower:
                    extracted_skills.append(skill.title())
        
        # Remove duplicates while preserving order
        unique_skills = []
        for skill in extracted_skills:
            if skill not in unique_skills:
                unique_skills.append(skill)
        
        return unique_skills
        
    except Exception as e:
        return []

@tool
def create_user_profile_json(user_data: Dict[str, Any]) -> str:
    """
    Create a structured JSON profile from user data.
    
    Args:
        user_data: Dictionary containing user information
    
    Returns:
        JSON string of structured user profile
    """
    try:
        # Create standardized profile structure
        profile = {
            'profile_id': f"user_{int(time.time())}",
            'created_at': datetime.now().isoformat(),
            'personal_info': {
                'name': user_data.get('name', ''),
                'experience_level': user_data.get('experience_level', 'beginner'),
                'career_stage': user_data.get('career_stage', 'student')
            },
            'technical_profile': {
                'skills': user_data.get('skills', []),
                'preferred_technologies': user_data.get('preferred_technologies', []),
                'programming_languages': user_data.get('programming_languages', [])
            },
            'interests_and_goals': {
                'domains_of_interest': user_data.get('interests', []),
                'career_goals': user_data.get('career_goals', []),
                'project_preferences': user_data.get('project_preferences', {})
            },
            'constraints': {
                'time_commitment': user_data.get('time_commitment', 'moderate'),
                'budget_range': user_data.get('budget_range', 'free'),
                'collaboration_preference': user_data.get('collaboration_preference', 'solo')
            },
            'metadata': {
                'profile_completeness': calculate_profile_completeness(user_data),
                'last_updated': datetime.now().isoformat()
            }
        }
        
        return json.dumps(profile, indent=2)
        
    except Exception as e:
        return json.dumps({'error': str(e)})

def calculate_profile_completeness(user_data: Dict[str, Any]) -> float:
    """Calculate how complete the user profile is (0.0 to 1.0)."""
    total_fields = 10
    completed_fields = 0
    
    fields_to_check = [
        'name', 'experience_level', 'skills', 'interests', 'career_goals',
        'preferred_technologies', 'time_commitment', 'project_preferences',
        'programming_languages', 'career_stage'
    ]
    
    for field in fields_to_check:
        if field in user_data and user_data[field]:
            completed_fields += 1
    
    return completed_fields / total_fields

# =============================================================================
# PROJECT GENERATION AND RANKING TOOLS
# =============================================================================

@tool
def generate_project_ideas(user_profile: str, domain: str = "general") -> List[Dict[str, Any]]:
    """
    Generate project ideas based on user profile and domain.
    
    Args:
        user_profile: JSON string of user profile
        domain: Specific domain to focus on (optional)
    
    Returns:
        List of project idea dictionaries
    """
    try:
        profile = json.loads(user_profile)
        
        # Base project templates categorized by domain
        project_templates = {
            'ai_ml': [
                {
                    'title': 'Intelligent Document Processing System',
                    'description': 'Build an AI system that can automatically extract, classify, and summarize information from various document types',
                    'difficulty': 'intermediate',
                    'technologies': ['Python', 'OpenAI API', 'FastAPI', 'React'],
                    'estimated_time': '4-6 weeks',
                    'impact_score': 8.5
                },
                {
                    'title': 'Multi-Modal Content Creator',
                    'description': 'Develop an AI agent that creates content across text, images, and audio based on user prompts',
                    'difficulty': 'advanced',
                    'technologies': ['Python', 'Stable Diffusion', 'GPT-4', 'Audio APIs'],
                    'estimated_time': '6-8 weeks',
                    'impact_score': 9.0
                }
            ],
            'web_development': [
                {
                    'title': 'Real-time Collaboration Platform',
                    'description': 'Create a platform for teams to collaborate on projects with live editing, video calls, and task management',
                    'difficulty': 'intermediate',
                    'technologies': ['React', 'Node.js', 'Socket.io', 'MongoDB'],
                    'estimated_time': '6-8 weeks',
                    'impact_score': 8.0
                },
                {
                    'title': 'Progressive Web App for Local Services',
                    'description': 'Build a PWA that connects local service providers with customers, featuring offline functionality',
                    'difficulty': 'intermediate',
                    'technologies': ['React', 'Service Workers', 'IndexedDB', 'Geolocation API'],
                    'estimated_time': '5-7 weeks',
                    'impact_score': 7.5
                }
            ],
            'data_science': [
                {
                    'title': 'Predictive Analytics Dashboard',
                    'description': 'Create an interactive dashboard that provides predictive insights for business metrics',
                    'difficulty': 'intermediate',
                    'technologies': ['Python', 'Streamlit', 'Plotly', 'Pandas'],
                    'estimated_time': '4-6 weeks',
                    'impact_score': 8.0
                },
                {
                    'title': 'Automated Report Generation System',
                    'description': 'Build a system that automatically generates comprehensive reports from raw data sources',
                    'difficulty': 'intermediate',
                    'technologies': ['Python', 'Pandas', 'Matplotlib', 'Jinja2'],
                    'estimated_time': '3-5 weeks',
                    'impact_score': 7.0
                }
            ],
            'mobile_development': [
                {
                    'title': 'AR-Enhanced Learning App',
                    'description': 'Develop a mobile app that uses augmented reality to make learning interactive and engaging',
                    'difficulty': 'advanced',
                    'technologies': ['React Native', 'ARKit/ARCore', 'Firebase'],
                    'estimated_time': '8-10 weeks',
                    'impact_score': 9.0
                }
            ]
        }
        
        # Select relevant projects based on user profile
        user_interests = profile.get('interests_and_goals', {}).get('domains_of_interest', [])
        user_skills = profile.get('technical_profile', {}).get('skills', [])
        experience_level = profile.get('personal_info', {}).get('experience_level', 'beginner')
        
        selected_projects = []
        
        # If domain specified, focus on that
        if domain != "general" and domain in project_templates:
            selected_projects.extend(project_templates[domain])
        else:
            # Select from all domains based on interests
            for domain_name, projects in project_templates.items():
                if any(interest.lower() in domain_name.lower() for interest in user_interests):
                    selected_projects.extend(projects[:2])  # Limit per domain
        
        # If no matches or too few, add some general projects
        if len(selected_projects) < 5:
            for projects in project_templates.values():
                selected_projects.extend(projects[:1])
        
        # Filter by experience level
        filtered_projects = []
        for project in selected_projects:
            project_difficulty = project.get('difficulty', 'intermediate')
            if should_include_project(experience_level, project_difficulty):
                filtered_projects.append(project)
        
        return filtered_projects[:15]  # Return top 15 for ranking
        
    except Exception as e:
        return [{'error': str(e)}]

def should_include_project(user_level: str, project_difficulty: str) -> bool:
    """Determine if a project matches user's experience level."""
    level_mapping = {
        'beginner': ['beginner'],
        'intermediate': ['beginner', 'intermediate'],
        'advanced': ['beginner', 'intermediate', 'advanced'],
        'expert': ['beginner', 'intermediate', 'advanced', 'expert']
    }
    
    return project_difficulty in level_mapping.get(user_level, ['beginner'])

@tool
def rank_projects(projects: List[Dict[str, Any]], user_profile: str) -> List[Dict[str, Any]]:
    """
    Rank projects based on user profile and scoring criteria.
    
    Args:
        projects: List of project dictionaries
        user_profile: JSON string of user profile
    
    Returns:
        List of ranked projects with scores
    """
    try:
        profile = json.loads(user_profile)
        
        scored_projects = []
        
        for project in projects:
            if 'error' in project:
                continue
                
            score = calculate_project_score(project, profile)
            
            scored_project = project.copy()
            scored_project['relevance_score'] = score['relevance']
            scored_project['feasibility_score'] = score['feasibility']
            scored_project['impact_score'] = project.get('impact_score', 7.0)
            scored_project['overall_score'] = (
                score['relevance'] * 0.4 + 
                score['feasibility'] * 0.3 + 
                project.get('impact_score', 7.0) * 0.3
            )
            
            scored_projects.append(scored_project)
        
        # Sort by overall score (descending)
        ranked_projects = sorted(scored_projects, key=lambda x: x['overall_score'], reverse=True)
        
        return ranked_projects[:10]  # Return top 10
        
    except Exception as e:
        return [{'error': str(e)}]

def calculate_project_score(project: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, float]:
    """Calculate relevance and feasibility scores for a project."""
    
    # Extract user data
    user_skills = profile.get('technical_profile', {}).get('skills', [])
    user_interests = profile.get('interests_and_goals', {}).get('domains_of_interest', [])
    experience_level = profile.get('personal_info', {}).get('experience_level', 'beginner')
    time_commitment = profile.get('constraints', {}).get('time_commitment', 'moderate')
    
    # Calculate relevance score (0-10)
    relevance_score = 0.0
    
    # Check technology overlap
    project_techs = project.get('technologies', [])
    tech_overlap = len(set([skill.lower() for skill in user_skills]) & 
                      set([tech.lower() for tech in project_techs]))
    relevance_score += min(tech_overlap * 2, 5)  # Max 5 points for tech overlap
    
    # Check interest alignment
    project_title = project.get('title', '').lower()
    project_desc = project.get('description', '').lower()
    interest_matches = sum(1 for interest in user_interests 
                          if interest.lower() in project_title or interest.lower() in project_desc)
    relevance_score += min(interest_matches * 2, 3)  # Max 3 points for interests
    
    # Base relevance
    relevance_score += 2  # Base score
    
    # Calculate feasibility score (0-10)
    feasibility_score = 5.0  # Base feasibility
    
    # Adjust for experience level
    difficulty_level = project.get('difficulty', 'intermediate')
    if experience_level == 'beginner' and difficulty_level == 'advanced':
        feasibility_score -= 2
    elif experience_level == 'advanced' and difficulty_level == 'beginner':
        feasibility_score += 1
    
    # Adjust for time commitment
    estimated_time = project.get('estimated_time', '4-6 weeks')
    if 'week' in estimated_time.lower():
        weeks = extract_max_weeks(estimated_time)
        if time_commitment == 'low' and weeks > 6:
            feasibility_score -= 2
        elif time_commitment == 'high' and weeks < 4:
            feasibility_score += 1
    
    return {
        'relevance': min(max(relevance_score, 0), 10),
        'feasibility': min(max(feasibility_score, 0), 10)
    }

def extract_max_weeks(time_str: str) -> int:
    """Extract maximum number of weeks from time string."""
    import re
    numbers = re.findall(r'\d+', time_str)
    return int(numbers[-1]) if numbers else 6

# =============================================================================
# PRESENTATION AND OUTPUT TOOLS
# =============================================================================

@tool
def format_project_presentation(projects: List[Dict[str, Any]]) -> str:
    """
    Format ranked projects into a presentation-ready format.
    
    Args:
        projects: List of ranked project dictionaries
    
    Returns:
        Formatted string presentation of projects
    """
    try:
        if not projects:
            return "No projects found matching your profile."
        
        presentation = []
        presentation.append("🚀 TOP 10 PERSONALIZED PROJECT RECOMMENDATIONS\n")
        presentation.append("=" * 50 + "\n")
        
        for i, project in enumerate(projects[:10], 1):
            if 'error' in project:
                continue
                
            presentation.append(f"#{i}. {project.get('title', 'Untitled Project')}")
            presentation.append(f"📊 Score: {project.get('overall_score', 0):.1f}/10")
            presentation.append(f"📝 Description: {project.get('description', 'No description available')}")
            presentation.append(f"🔧 Technologies: {', '.join(project.get('technologies', []))}")
            presentation.append(f"⏱️  Estimated Time: {project.get('estimated_time', 'Not specified')}")
            presentation.append(f"📈 Difficulty: {project.get('difficulty', 'Not specified').title()}")
            presentation.append(f"💡 Impact Score: {project.get('impact_score', 0)}/10")
            presentation.append(f"🎯 Relevance: {project.get('relevance_score', 0):.1f}/10")
            presentation.append(f"✅ Feasibility: {project.get('feasibility_score', 0):.1f}/10")
            presentation.append("\n" + "-" * 40 + "\n")
        
        presentation.append("💡 Pro Tips:")
        presentation.append("• Start with projects scoring 8+ in feasibility")
        presentation.append("• Consider your current time availability")
        presentation.append("• Focus on technologies you want to learn")
        presentation.append("• Build a portfolio with diverse project types")
        
        return "\n".join(presentation)
        
    except Exception as e:
        return f"Error formatting presentation: {str(e)}"

@tool
def save_project_recommendations(projects: List[Dict[str, Any]], filename: str = None) -> Dict[str, Any]:
    """
    Save project recommendations to a file.
    
    Args:
        projects: List of project dictionaries
        filename: Optional filename (auto-generated if not provided)
    
    Returns:
        Dictionary with save status and file info
    """
    try:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"project_recommendations_{timestamp}.json"
        
        # Prepare data for saving
        save_data = {
            'generated_at': datetime.now().isoformat(),
            'total_projects': len(projects),
            'projects': projects
        }
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        return {
            'success': True,
            'filename': filename,
            'projects_saved': len(projects),
            'message': f'Successfully saved {len(projects)} projects to {filename}'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': 'Failed to save project recommendations'
        }

@tool
def export_to_csv(projects: List[Dict[str, Any]], filename: str = None) -> Dict[str, Any]:
    """
    Export project recommendations to CSV format.
    
    Args:
        projects: List of project dictionaries
        filename: Optional CSV filename
    
    Returns:
        Dictionary with export status
    """
    try:
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"projects_{timestamp}.csv"
        
        if not projects:
            return {'success': False, 'error': 'No projects to export'}
        
        # Prepare CSV data
        csv_data = []
        for i, project in enumerate(projects, 1):
            if 'error' in project:
                continue
                
            csv_data.append({
                'Rank': i,
                'Title': project.get('title', ''),
                'Description': project.get('description', ''),
                'Technologies': ', '.join(project.get('technologies', [])),
                'Difficulty': project.get('difficulty', ''),
                'Estimated_Time': project.get('estimated_time', ''),
                'Overall_Score': project.get('overall_score', 0),
                'Relevance_Score': project.get('relevance_score', 0),
                'Feasibility_Score': project.get('feasibility_score', 0),
                'Impact_Score': project.get('impact_score', 0)
            })
        
        # Write CSV
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            if csv_data:
                fieldnames = csv_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
        
        return {
            'success': True,
            'filename': filename,
            'records_exported': len(csv_data)
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

# =============================================================================
# AVAILABLE TOOLS LIST
# =============================================================================

available_tools = [
    search_github_trending,
    search_tech_news,
    validate_user_input,
    extract_skills_from_text,
    create_user_profile_json,
    generate_project_ideas,
    rank_projects,
    format_project_presentation,
    save_project_recommendations,
    export_to_csv
]