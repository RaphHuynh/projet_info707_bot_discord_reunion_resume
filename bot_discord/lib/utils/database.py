import sqlite3

# Fonction pour récupérer les participants d'un résumé
def fetch_attendees_for_resume(sqlite_connection, resume_id):
    query = """
        SELECT u.discord_tag
        FROM meeting_app_resume_attendees a
        JOIN discord_login_discorduser u ON a.discorduser_id = u.id
        WHERE a.resume_id = ?
    """
    results = sqlite_connection.execute(query, (resume_id,)).fetchall()
    return [result[0] for result in results]

# Fonction pour récupérer un résumé de réunion spécifique par son titre
def fetch_resume_by_title(sqlite_connection, user_id, title):
    query = """
        SELECT r.id, r.title, r.date, r.duration, r.text_sum_up
        FROM meeting_app_resume r
        JOIN meeting_app_resume_attendees a ON r.id = a.resume_id
        WHERE a.discorduser_id = ? AND r.title = ?
    """
    result = sqlite_connection.execute(query, (user_id, title)).fetchone()

    if result:
        # Récupérer les participants
        resume_id = result[0]
        attendees = fetch_attendees_for_resume(sqlite_connection, resume_id)

        return {
            "id": result[0],
            "title": result[1],
            "date": result[2],
            "duration": result[3],
            "text_sum_up": result[4],
            "attendees": attendees,
        }
    return None

# Fonction pour récupérer les titres des réunions de l'utilisateur
def fetch_titles_by_user(sqlite_connection, user_id):
    query = """
        SELECT DISTINCT r.title
        FROM meeting_app_resume r
        JOIN meeting_app_resume_attendees a ON r.id = a.resume_id
        WHERE a.discorduser_id = ?
    """
    results = sqlite_connection.execute(query, (user_id,)).fetchall()
    return [result[0] for result in results]

def fetch_messages_by_resume_title(sqlite_connection, title):
    query = """
        SELECT u.discord_tag, m.content, m.date
        FROM meeting_app_resume r
        JOIN meeting_app_resume_messages rm ON r.id = rm.resume_id
        JOIN meeting_app_message m ON rm.message_id = m.id
        JOIN discord_login_discorduser u ON m.author_id = u.id
        WHERE r.title = ?
    """
    results = sqlite_connection.execute(query, (title,)).fetchall()
    
    # Retourner une liste de dictionnaires contenant discord_tag, message, et datetime
    return [
        {
            "discord_tag": result[0],
            "message": result[1],
            "datetime": result[2]
        }
        for result in results
    ]