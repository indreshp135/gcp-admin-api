from google.oauth2 import service_account
from googleapiclient.discovery import build

# Replace with your actual file path
SERVICE_ACCOUNT_FILE = 'sa.json'

# Scopes required for Directory API
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user.readonly']

# Your super admin email
DELEGATED_ADMIN = 'ip@indresh.me'


def main():
    # Create credentials with domain-wide delegation
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    delegated_creds = credentials.with_subject(DELEGATED_ADMIN)

    # Build service with impersonated credentials
    service = build('admin', 'directory_v1', credentials=delegated_creds)

    # Call the Admin SDK Directory API
    print("Getting the first 10 users in the domain")
    results = service.users().list(customer='my_customer',
                                   maxResults=10, orderBy='email').execute()
    users = results.get('users', [])

    if not users:
        print('No users found.')
    else:
        print('Users:')
        for user in users:
            print(f"{user['primaryEmail']} ({user['name']['fullName']})")


if __name__ == '__main__':
    main()
