# Check if the user has a specific role
has_role(user, role_name) if
    role_name in user.roles;

# Define permissions
# Allow users with the "admin" role to perform any action
allow(user, _, _) if
    has_role(user, "admin");

# Allow users with specific roles to perform matching actions
allow(user, action, _) if
    has_role(user, action);