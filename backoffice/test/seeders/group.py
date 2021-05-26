from backoffice.business_logic.group import GroupLogic


def seed_group(user_login_code, group_data):
    """
    Create data for our athlete.
    """
    group_logic = GroupLogic()
    slug_name = group_data.get('slug_name')
    group_logic.create(user_login_code, group_data)
    group = group_logic.retrieve(user_login_code, slug_name)
    group_code = group.get('group_code')
    result = {}
    result['group_code'] = group_code

    return result
