from django.forms import model_to_dict
from django.utils.timezone import now

from backoffice import models
from backoffice.utils.constant import Status, URL, RoleLevel
from backoffice.utils.exceptions import EntityNotFound, UnAuthorized, UsedInvitation, DuplicatedRecord, \
    MembersLimitExceeded


class InvitationLogic():
    """
    This manage the invitation logic
    def create(): Create a new invitation, with user_login_code and the slug_name of the group to be invited with
    def list(): list all the invitations using user_code and slug_name and
    def activate(): activate the invitation, check members_limit and if the user it is part of the group already.
    """

    def __init__(self):
        self.fields = ['status', 'is_used']

    def create(self, user_login_code, slug_name):
        user = models.UserLogin.objects.get_user_by_code(user_login_code)
        if not user:
            raise EntityNotFound(
                f'User with code {user_login_code} not found'
            )
        group = models.Group.objects.get_group_by_group_slug_name(user_login_code, slug_name)
        if not group:
            raise EntityNotFound(
                f'Group with slug name {slug_name} not found.'
            )
        invitation = models.Invitation()
        invitation.group = group
        invitation.issued_by = user
        invitation.status = Status.ACTIVE.value
        membership = models.Membership.objects.get_membership_data_by_user_code_slug_name(user_login_code, slug_name)
        members_quantity = models.Membership.objects.get_membership_count_by_group_slug_name(slug_name)
        if membership.remaining_invitations == 0 or membership.status == 0 or membership.role == 1 or \
                membership.group.members_limit < members_quantity:
            raise UnAuthorized(
                'You do not have remaining invitations or the privilege to invite or the group it is full')
        new_invitation = models.Invitation.objecs.save(invitation)
        membership.remaining_invitations -= 1
        models.Membership.objects.save(membership)
        return self.__mapped_detailed_invitation(new_invitation)

    def list(self, user_login_code, slug_name):
        user = models.UserLogin.objects.get_user_by_code(user_login_code)
        if not user:
            raise EntityNotFound(
                f'User with code {user_login_code} not found'
            )
        group = models.Group.objects.get_group_by_group_slug_name(user_login_code, slug_name)
        if not group:
            raise EntityNotFound(
                f'Group with slug name {slug_name} not found.'
            )
        invitations = models.Invitation.objecs.get_all_Invitations(user_login_code, slug_name)
        invitations_list = []
        for invitation in invitations:
            invitations_list.append(self.__mapped_detailed_invitation(invitation))
        return invitations_list

    def activate(self, invitation_code, request):
        invitation = models.Invitation.objecs.get_invitation_by_code(invitation_code)
        if not invitation:
            raise EntityNotFound(
                f'Invitation with invitation code {invitation_code} not found'
            )
        if invitation.is_used:
            raise UsedInvitation(
                f'Invitation with code {invitation_code} has been used'
            )
        user_login_code = request.user['user_login_code']
        invited_user = models.UserLogin.objects.get_user_by_code(user_login_code)
        if not invited_user:
            raise EntityNotFound(
                f'User with code {user_login_code} not found'
            )
        # updating invitation
        invitation.is_used = True
        invitation.used_at = now()
        invitation.used_by = invited_user
        models.Invitation.objecs.save(invitation)
        # creating new member
        invitation_dict = self.__mapped_invitation(invitation)
        issued_by = models.UserLogin.objects.get_user_by_code(invitation_dict['issued_by'])
        group = models.Group.objects.get_group_by_group_code(invitation_dict['group_code'])
        # update membership of issued_by
        issued_by_membership = models.Membership.objects.get_membership_by_user_code_group_code(
            invitation_dict['issued_by'],
            invitation_dict['group_code'])
        print('50'*50)
        print(type(issued_by_membership))
        print(issued_by_membership)
        if issued_by_membership:
            if issued_by_membership.remaining_invitations == 0:
                raise MembersLimitExceeded('The user can have no longer invite')
            issued_by_membership.used_invitations += 1
            issued_by_membership.remaining_invitations -= 1
            models.Membership.objects.save(issued_by_membership)

        new_membership = models.Membership()

        new_membership.group = group
        new_membership.invited_by = issued_by
        new_membership.user = invited_user
        new_membership.role = RoleLevel.USER.value
        new_membership.status = Status.ACTIVE.value
        # Check member limits and if there is a duplicate member
        member_limit = models.Membership.objects.get_membership_count_by_group_slug_name(invitation_dict['group'])
        if member_limit >= group.members_limit:
            raise MembersLimitExceeded('Members limit exceeded.')
        already_member = models.Membership.objects.get_membership_by_user_code_group_code(user_login_code,
                                                                                          invitation_dict['group_code'])
        if already_member:
            raise DuplicatedRecord('You already belong to this group.')
        # Add new member
        member_added = models.Membership.objects.save(new_membership)
        return self.__mapped_membership(member_added)

    def __mapped_invitation(self, invitation):
        invitation_dict = model_to_dict(invitation, fields=self.fields)
        invitation_dict['group'] = str(invitation.group.slug_name)
        invitation_dict['group_code'] = str(invitation.group.group_code)
        invitation_dict['issued_by'] = str(invitation.issued_by.user_login_code)
        return invitation_dict

    def __mapped_detailed_invitation(self, invitation):
        invitation_dict = model_to_dict(invitation, fields=self.fields)
        invitation_dict['invitation_code'] = str(invitation.invitation_code)
        invitation_dict['group'] = str(invitation.group.slug_name)
        invitation_dict['group_code'] = str(invitation.group.group_code)
        invitation_dict['issued_by'] = str(invitation.issued_by.name)
        invitation_dict['used_by'] = None if invitation.used_by == None else str(invitation.used_by.name)
        invitation_dict['url'] = str(URL.ACTIVATION + str(invitation.invitation_code) + '/')
        return invitation_dict

    def __mapped_membership(self, member):
        member_dict = model_to_dict(member, fields=self.fields)
        member_dict['membership_code'] = str(member.membership_code)
        member_dict['role'] = str(RoleLevel(member.role))
        member_dict['invited_by'] = str(member.invited_by.name)
        member_dict['group'] = str(member.group.slug_name)
        member_dict['status'] = str(Status(member.status))
        return member_dict
