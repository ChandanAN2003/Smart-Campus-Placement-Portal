from database import db

def add_points(user_id, points, reason):
    """
    Add points to a user's score and check for new badges.
    """
    try:
        # 1. Update score
        db.execute_query(
            "UPDATE users SET score = score + %s WHERE id = %s",
            (points, user_id)
        )
        
        # 2. Get new total score
        user = db.execute_query("SELECT score FROM users WHERE id = %s", (user_id,), fetch_one=True)
        new_score = user['score']
        
        # 3. Check for Badges
        # Get all badges where criteria is met but not yet awarded
        potential_badges = db.execute_query(
            """
            SELECT b.* FROM badges b
            WHERE b.min_score <= %s
            AND b.id NOT IN (SELECT badge_id FROM user_badges WHERE user_id = %s)
            """,
            (new_score, user_id),
            fetch_all=True
        )
        
        new_badges_awarded = []
        for badge in potential_badges:
            db.execute_query(
                "INSERT INTO user_badges (user_id, badge_id) VALUES (%s, %s)",
                (user_id, badge['id'])
            )
            new_badges_awarded.append(badge['name'])
            
        return {
            'success': True, 
            'new_score': new_score, 
            'badges_awarded': new_badges_awarded
        }
        
    except Exception as e:
        print(f"Gamification Error: {e}")
        return {'success': False, 'error': str(e)}

def get_leaderboard(limit=10):
    """Get top scoring students"""
    return db.execute_query(
        "SELECT name as full_name, score, department FROM users WHERE role='student' ORDER BY score DESC LIMIT %s",
        (limit,),
        fetch_all=True
    )

def get_user_badges(user_id):
    """Get badges for a specific user"""
    return db.execute_query(
        """
        SELECT b.name, b.icon, b.description 
        FROM badges b
        JOIN user_badges ub ON b.id = ub.badge_id
        WHERE ub.user_id = %s
        """,
        (user_id,),
        fetch_all=True
    )
