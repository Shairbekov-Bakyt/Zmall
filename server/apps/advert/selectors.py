from advert.models import Comment

def recrursive_sql_query():
    query = '''with recursive tree (id, text, advert_id, parent_id, user_id)
            as (select id, text, advert_id, parent_id, user_id from advert_comment
            where parent_id is null
        union all
           select advert_comment.id, advert_comment.text, advert_comment.advert_id,
                  advert_comment.parent_id, advert_comment.user_id from advert_comment
             inner join tree on tree.id = advert_comment.parent_id)
        select id, text, advert_id, parent_id, user_id from tree
    '''
    comments = Comment.objects.raw(query)
    for comment in comments:
        print(comment)


