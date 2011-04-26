def permissions(request):
    return {
        "is_reviewer": request.user.groups.filter(name="reviewers").exists(),
        "is_reviewer_tutorials": request.user.groups.filter(name="reviewers-tutorials").exists(),
        "is_reviewer_admin": request.user.groups.filter(name="reviewers-admins").exists(),
    }