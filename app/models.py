from .database import supabase_db
from config import Config
from .utils import hash_password, check_password, decrypt, generate_tokens
from datetime import datetime
from .utils import StreakManager

class Category:
    def __init__(self):
        self.categories_table = supabase_db.table(Config.USERS_CATEGORIES_TABLE_NAME)
        
    def get(self, username):
        data = self.categories_table.select("*").eq("username", username).execute()

        if len(data.data) == 0:
            categories = None
        else:
            categories = data.data[0]['categories']

        return {
            "categories" : categories
        }
    def add(self, username, category_name):
        existing_categories = self.get(username).get('categories') or []

        updated_categories = list(set(existing_categories + [category_name, 'Daily']))

        try:
            if existing_categories:
                self.categories_table.update({
                    "categories": updated_categories
                }).eq("username", username).execute()
            else:
                self.categories_table.insert({
                    "username": username,
                    "categories": updated_categories
                }).execute()
            return True
        except Exception as e:
            print(e)
            return False


class User:
    def __init__(self):
        self.users_table = supabase_db.table(Config.USERS_TABLE_NAME)
        self.category = Category()

    def get_user(self, username):
        data = self.users_table.select("*").eq("username", username).execute()

        return None if len(data.data) == 0 else data.data[0]
    
    def get_user_info(self, username):

        user_data = self.get_user(username)
        user_categories = self.category.get(username)

        return user_data | user_categories
    
    @staticmethod
    def check_password_hash(password, password_hash):
        return check_password(password, password_hash)
    
    def add_user(self, username, password, email):
        try:
            self.users_table.insert(
                {
                    "username" : username,
                    "password" : hash_password(password),
                    "email" : email
                }
            ).execute()
            return True
        except:
            return False
    
    def add_google_user(self, email, username, profile_picture):
        try:
            self.users_table.insert(
                {
                    "username" : username,
                    "password" : "",
                    "email" : email,
                    "profile_picture" : profile_picture
                }
            ).execute()
            
            return True
        except Exception as e:
            print(e)
            return False
        
    def get_all_users(self):
        data = self.users_table.select("*").execute()
        return data.data



class Entry:
    def __init__(self):
        self.user = User()
        self.entries_table = supabase_db.table(Config.USERS_ENTRIES_TABLE_NAME)

    def add(self, username, title, description, emoji, category, sharing, slug, title_search_token, year, month, day):
        try:
            self.entries_table.insert(
                    {
                        "username" : username,
                        "title" : title,
                        "description" : description,
                        "emoji" : emoji,
                        "category" : category,
                        "sharing" : sharing,
                        "slug" : slug,
                        "title_search_token" : title_search_token,
                        "year" : year,
                        "month" : month,
                        "day" : day,
                    }
            ).execute()

            return True
        except Exception as e:
            print(e)
            return False
        
    def get(self, username, query = None):
        try:
            
            if query:
                data = self.entries_table.select("*").eq("username", username).contains("title_search_token", generate_tokens(query)).execute()
            else:
                data = self.entries_table.select("*").eq("username", username).execute()
            
            new_data = [
                {
                    "created_at" : entry.get('created_at'),
                    "username" : entry.get('username'),
                    "title" : decrypt(entry.get('title')),
                    "description" : decrypt(entry.get('description')),
                    "emoji" : entry.get('emoji'),
                    "category" : entry.get('category'),
                    "sharing" : entry.get('sharing'),
                    "slug" : entry.get('slug'),
                    "post_id" : entry.get('post_id'),
                    "year" : entry.get('year'),
                    "month" : entry.get('month'),
                    "day" : entry.get('day'),
                } 
                for entry in data.data
            ]

            return new_data

        except Exception as e:
            print(e)
            return []
        
            
class Streak:
    def __init__(self, username):
        self.username = username
        self.streaks_table = supabase_db.table(Config.USERS_STREAKS_TABLE_NAME)
        self.available_streaks, self.modified_date = self.get_streak_data(username)
        self.streak_manager = StreakManager(self.modified_date)

    @staticmethod
    def get_now():
        now = datetime.now()
        return "{:04d}-{:02d}-{:02d}".format(
                now.year, now.month, now.day
            )

    def get_streak_data(self, username):
        data = self.streaks_table.select("*").eq("username", username).execute().data

        if not data:
            self.init(username)
            return 0, self.get_now()
        
        return data[0].get('count'), data[0].get('modified_at')

    def check(self):
        error = True
        if (self.streak_manager.can_add_streak()) or self.available_streaks == 0:
            error = not error

        if (self.streak_manager.is_beyond_48hrs(self.modified_date)):

            # Make it go back to 0

            error = not error
            self.available_streaks = 0
            self.streaks_table.update({
                        "modified_at": self.get_now(),
                        "count" : 0
                }).eq("username", self.username).execute()

        else:
            error = not error

        can_add_streak = False

        if (self.streak_manager.can_add_streak()) or self.available_streaks == 0:
            can_add_streak = True

        return {
            "available_streaks" : self.available_streaks,
            "can_add_streak" : can_add_streak
        }
        


    def add(self):

        error = True
        message = "You have already checked-in."

        if (self.streak_manager.can_add_streak()) or self.available_streaks == 0:

            try:
                self.streaks_table.update({
                        "modified_at": self.get_now(),
                        "count" : int(self.available_streaks) + 1
                }).eq("username", self.username).execute()

                error = False
                message = "Streak updated successfully"
         
            except Exception as e:
                print(e)
                error = True
                message = "Something went wrong"

        return {
            "error" : error,
            "message" : message
        }

    def init(self, username):
        self.streaks_table.insert({
            "username": username,
            "modified_at":self.get_now(),
            "count" : 0
        }).execute()
