from advert.models import Comment, Advert


def recursive_sql_query():
    sql = """with recursive tree (id, text, advert_id, parent_id, user_id)
            as (select id, text, advert_id, parent_id, user_id from advert_comment
            where parent_id is null
        union all
           select advert_comment.id, advert_comment.text, advert_comment.advert_id,
                  advert_comment.parent_id, advert_comment.user_id from advert_comment
             inner join tree on tree.id = advert_comment.parent_id)
        select id, text, advert_id, parent_id, user_id from tree
    """

    return Comment.objects.raw(sql)


def advert_with_select_related_filter(field):
    return Advert.objects.select_related("category", "sub_category").filter(
        status=field
    )
