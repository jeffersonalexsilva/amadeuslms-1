from django.db.models import Q

from .models import SubjectPost

from users.models import User

def getSpaceUsers(user, post):
	if post._my_subclass == "generalpost":
		return User.objects.all().exclude(id = user)
	elif post._my_subclass == "categorypost":
		space = post.get_space()

		return User.objects.filter(Q(is_staff = True) | Q(coordinators__id = space) | Q(professors__category__id = space) | Q(subject_student__category__id = space)).exclude(id = user).distinct()
	elif post._my_subclass == "subjectpost":
		space = post.get_space()

		if post.subjectpost.resource:
			resource = post.subjectpost.resource

			return User.objects.filter(Q(is_staff = True) | Q(professors__id = space) | Q(coordinators__subject_category__id = space) | Q(resource_students = resource) | Q(group_participants__resource_groups = resource) | (Q(subject_student__id = space) & Q(subject_student__topic_subject__resource_topic = resource) & Q(subject_student__topic_subject__resource_topic__all_students = True))).exclude(id = user).distinct()
		else:
			return User.objects.filter(Q(is_staff = True) | Q(professors__id = space) | Q(coordinators__subject_category__id = space) | Q(subject_student__id = space)).exclude(id = user).distinct()

	return None

def getSubjectPosts(subject, user, favorites, mines):
	if not favorites:
		if mines:
			if not user.is_staff:
				posts = SubjectPost.objects.extra(select = {"most_recent": "greatest(mural_mural.last_update, (select max(mural_comment.last_update) from mural_comment where mural_comment.post_id = mural_subjectpost.mural_ptr_id))"}).filter(
					Q(space__id = subject) & Q(mural_ptr__user = user) & (
					Q(space__category__coordinators = user) | 
					Q(space__professor = user) | 
					Q(resource__isnull = True) |
					(Q(resource__isnull = False) & (Q(resource__all_students = True) | Q(resource__students = user) | Q(resource__groups__participants = user))))).distinct()
			else:
				posts = SubjectPost.objects.extra(select = {"most_recent": "greatest(mural_mural.last_update, (select max(mural_comment.last_update) from mural_comment where mural_comment.post_id = mural_subjectpost.mural_ptr_id))"}).filter(space__id = subject, mural_ptr__user = user)
		else:
			if not user.is_staff:
				posts = SubjectPost.objects.extra(select = {"most_recent": "greatest(mural_mural.last_update, (select max(mural_comment.last_update) from mural_comment where mural_comment.post_id = mural_subjectpost.mural_ptr_id))"}).filter(
					Q(space__id = subject) & (
					Q(space__category__coordinators = user) | 
					Q(space__professor = user) | 
					Q(resource__isnull = True) |
					(Q(resource__isnull = False) & (Q(resource__all_students = True) | Q(resource__students = user) | Q(resource__groups__participants = user))))).distinct()
			else:
				posts = SubjectPost.objects.extra(select = {"most_recent": "greatest(mural_mural.last_update, (select max(mural_comment.last_update) from mural_comment where mural_comment.post_id = mural_subjectpost.mural_ptr_id))"}).filter(space__id = subject)
	else:
		if mines:
			if not user.is_staff:
				posts = SubjectPost.objects.extra(select = {"most_recent": "greatest(mural_mural.last_update, (select max(mural_comment.last_update) from mural_comment where mural_comment.post_id = mural_subjectpost.mural_ptr_id))"}).filter(
					Q(space__id = subject) & Q(favorites_post__isnull = False) & Q(favorites_post__user = user) & Q(mural_ptr__user = user) & (
					Q(space__category__coordinators = user) | 
					Q(space__professor = user) | 
					Q(resource__isnull = True) |
					(Q(resource__isnull = False) & (Q(resource__all_students = True) | Q(resource__students = user) | Q(resource__groups__participants = user))))).distinct()
			else:
				posts = SubjectPost.objects.extra(select = {"most_recent": "greatest(mural_mural.last_update, (select max(mural_comment.last_update) from mural_comment where mural_comment.post_id = mural_subjectpost.mural_ptr_id))"}).filter(space__id = subject, favorites_post__isnull = False, favorites_post__user = user, mural_ptr__user = user)
		else:
			if not user.is_staff:
				posts = SubjectPost.objects.extra(select = {"most_recent": "greatest(mural_mural.last_update, (select max(mural_comment.last_update) from mural_comment where mural_comment.post_id = mural_subjectpost.mural_ptr_id))"}).filter(
					Q(space__id = subject) & Q(favorites_post__isnull = False) & Q(favorites_post__user = user) & (
					Q(space__category__coordinators = user) | 
					Q(space__professor = user) | 
					Q(resource__isnull = True) |
					(Q(resource__isnull = False) & (Q(resource__all_students = True) | Q(resource__students = user) | Q(resource__groups__participants = user))))).distinct()
			else:
				posts = SubjectPost.objects.extra(select = {"most_recent": "greatest(mural_mural.last_update, (select max(mural_comment.last_update) from mural_comment where mural_comment.post_id = mural_subjectpost.mural_ptr_id))"}).filter(space__id = subject, favorites_post__isnull = False, favorites_post__user = user)

	return posts