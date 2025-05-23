# This script contains user information to be used by the ADH-ME agent.

first_name = "John"
last_name = "Doe"
birth_date = "2000-12-31"
gender = "Male"
occupation = "University student"
interests = ["Technology", "Gaming", "Music", "Movies"]
preferred_communication_style = "Casual and friendly"
user_goals = ("- To improve productivity and manage time effectively, especially in academic settings.\n"
              "   - Become more organized and reduce procrastination.\n"
              "   - Manage household tasks and responsibilities efficiently.\n")


user_info = f"""
The following information is provided to the ADH-ME agent to help it understand the user's preferences and needs:

1. User's name: {first_name} {last_name}
2. User's birth date: {birth_date}
3. User's gender: {gender}
4. User's occupation: {occupation}
5. User's interests: {", ".join(interests)}
6. User's preferred communication style: {preferred_communication_style}
7. User's goals:
   {user_goals}

"""

def get_user_info():
    return user_info