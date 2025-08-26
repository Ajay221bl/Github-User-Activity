from urllib import request, error
import json
username = input("enter username: ")


class GithubActivity():
    def __init__(self, username):
        self.username = username

# retrieving events using the GitHub API
    def get_events(self):
        
        url = f"https://api.github.com/users/{username}/events"
        try:
            req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with request.urlopen(url) as response:
                if response.status == 200:
                    data = json.load(response)
                    return data
             
                
                else:
                    print(f"Error: Received status code {response.status}")
                    return None
        except error.HTTPError as e:
            if e.code == 404:
                print(f"Error: GitHub user '{username}' not found")
            elif e.code == 403:
                print(f"Error. API rate limit exceeded. Please wait and try again later.")
            else:
                print(f"Error: Failed to fetch data from Github API. Status code: {e.code}")
        return None
    
# producing well readable format from the above retrieved events
    def format_recent_activity(self, events):
        if not events:
            return ["No recent activity found or failed to fetch data."]
        output = []
        for event in events:
            event_type = event['type']
            repo_name = event['repo']['name']
            created_at = event['created_at']
        
            if event_type == 'PushEvent':
                commit_count = len(event['payload']['commits'])
                output.append(f"[{created_at}] Pushed {commit_count} commits to {repo_name}")
            elif event_type == 'CreateEvent':
                output.append(f"[{created_at}] Created a repository {repo_name}")
            elif event_type == "IssuesEvent":
                action = event['payload']['action']
                output.append(f"[{created_at}] {action.capitalize()} an issue in {repo_name}")

        return output
    
# saving the raw data retrieved to a json file    
    def copy_to_json(self, events):

        if not events:
            print("No data to save to JSON")
            return
        try:
            with open("output.json", "w") as file: 
                json.dump(events, file, indent=4)
            print("raw data wrote to json")
        except Exception as e:
            print(f"Failed to write to file: {e}")
    
  


    



if __name__ == "__main__":
    activity = GithubActivity(username)
    raw_events = activity.get_events()
# only run the code if there exist events
    if raw_events:
        formatted_activity = activity.format_recent_activity(raw_events)
        for line in formatted_activity:
            print(line)

        
        activity.copy_to_json(raw_events)




