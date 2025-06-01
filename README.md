AI Project Recommendation System 🌟

An interactive AI-powered system that recommends personalized project ideas based on users' skills, interests, and goals. This project leverages the CrewAI framework to orchestrate multiple AI agents, each specialized in a particular aspect of the recommendation process. 🚀

Table of Contents 📋

Introduction
Features
Architecture
Installation
Usage
Project Structure
Contributing
License
Contact


Introduction ℹ️
The AI Project Recommendation System is designed to help users discover project ideas tailored to their unique profiles. By leveraging a team of AI agents, the system engages users in a natural conversation to gather information about their background, skills, interests, and constraints. It then analyzes this data, generates a list of suitable project ideas, ranks them based on relevance and feasibility, and presents the top recommendations in an actionable format. 🎯
This system is ideal for students, professionals, and hobbyists looking to undertake meaningful projects that align with their goals and capabilities. Built with extensibility in mind, it uses the CrewAI framework to manage a collaborative team of AI agents powered by Google's Gemini API. 🌐

Features ✨

Interactive Onboarding: Engages users in a friendly, conversational process to collect comprehensive profile information. 🤝
Profile Analysis: Structures and validates user data into a detailed, machine-readable profile. 📊
Project Idea Generation: Creates diverse project ideas based on user profiles and real-time industry trends. 💡
Project Ranking: Prioritizes projects using a multi-dimensional scoring system (relevance, feasibility, impact). 🏆
Presentation: Delivers personalized recommendations with detailed explanations and next steps. 🎯
Extensibility: Supports integration of additional tools and agents to enhance functionality. 🛠️
Logging and Saving: Saves session data, recommendations, and feedback to the project_recommendation_output directory. 💾


Architecture 🏗️
The system is built using the CrewAI framework, which orchestrates a team of specialized AI agents working collaboratively. The architecture consists of the following agents:

User Onboarder: Collects user information through an interactive, natural conversation. 🗣️
User Profile Analyst: Analyzes and structures user data into a validated profile. 🔍
Project Generator: Generates diverse project ideas based on the user profile and industry trends. 🚀
Project Ranker: Ranks projects using a three-axis scoring system (Relevance, Feasibility, Impact). 📈
Presentation Specialist: Formats and presents the top recommendations in a compelling, actionable way. 📝

Each agent uses custom tools (e.g., GitHub trending search, profile validation) and operates sequentially, passing outputs to the next agent in the workflow. The system is powered by the Gemini API via the langchain-google-genai library and integrates with external services like Serper for enhanced functionality. ⚙️

Installation 🛠️
To set up the AI Project Recommendation System locally, follow these steps:

Clone the Repository: 📥
git clone https://github.com/naakaarafr/ai-project-recommendation-system.git
cd ai-project-recommendation-system


Install Dependencies: 📦Ensure you have Python 3.8 or higher installed. Then, install the required packages:
pip install -r requirements.txt


Set Up Environment Variables: 🔑Create a .env file in the project root and add the following API keys:
GOOGLE_API_KEY=your_google_api_key
SERPER_API_KEY=your_serper_api_key


Replace your_google_api_key with your Google API key for Gemini access.
Replace your_serper_api_key with your Serper API key (optional, for enhanced search capabilities).
Obtain these keys from their respective services if you don’t have them.


Verify Configuration: ✅Run the following command to check if the configuration is set up correctly:
python config.py

This will display the status of your API keys.



Usage 🚀
To start the interactive session, run the main script:
python main.py

The system will launch an interactive session with the following flow:

Welcome Message: Displays an introduction and instructions. 👋
Onboarding Phase: Asks questions about your background, skills, interests, and constraints. ❓
Answer naturally or use commands:
skip to skip a question. ⏭️
back to revisit the previous question. ⏮️
quit to exit the session. 🚪




Profile Analysis: Processes your responses into a structured profile. 📋
Project Generation: Creates a list of project ideas tailored to your profile. 💡
Ranking and Presentation: Ranks the ideas and presents the top recommendations. 🏅

All session data, including logs, recommendations, and feedback, are saved in the project_recommendation_output directory. 📂
Alternatively, you can run the crew directly with a predefined input:
python crew.py

This starts an interactive session where you can provide initial input and refine recommendations as needed. 🔄

Project Structure 📂
The project is organized as follows:
ai-project-recommendation-system/
├── main.py                        # Entry point for the interactive system 🚀
├── crew.py                        # Defines the CrewAI crew and workflow 🧠
├── agents.py                      # Defines the AI agents and their roles 🤖
├── tasks.py                       # Defines tasks for each agent 📝
├── tools.py                       # Custom tools for agents (e.g., GitHub search, profile validation) 🛠️
├── config.py                      # Handles configuration and API key management ⚙️
├── requirements.txt               # Lists project dependencies 📋
├── project_recommendation_output/ # Directory for output files (logs, recommendations, etc.) 💾
└── README.md                      # Project documentation 📘


main.py: Launches the interactive system with a step-by-step workflow. 🚀
crew.py: Manages the CrewAI setup and provides alternative execution modes. 🧠
agents.py: Contains agent definitions with roles, goals, and backstories. 🤖
tasks.py: Specifies detailed tasks for each agent in the workflow. 📝
tools.py: Implements custom tools used by agents for data processing and generation. 🛠️
config.py: Configures the environment and validates API keys. ⚙️


Contributing 🤝
Contributions are welcome! To contribute to the project, please follow these steps:

Fork the repository. 🍴
Create a new branch for your feature or bug fix: 🌿git checkout -b feature/your-feature-name


Make your changes and commit them with descriptive messages. ✍️
Push your changes to your fork: 📤git push origin feature/your-feature-name


Submit a pull request to the main repository. 📬

Please ensure your code adheres to the project's coding standards (e.g., PEP 8 for Python) and includes appropriate tests where applicable. ✅

License 📜
This project is licensed under the MIT License. See the LICENSE file for details. 📜

Contact 📞
For questions, suggestions, or issues, please contact the project maintainer:

GitHub: naakaarafr 👤
Email: your_email@example.com 📧

Feel free to open an issue on GitHub or reach out directly with feedback or inquiries! 💬

Happy coding, and enjoy discovering your next project with the AI Project Recommendation System! 🎉✨
