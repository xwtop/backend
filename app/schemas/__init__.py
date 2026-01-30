from app.schemas.auth_schema import *
from app.schemas.user_schema import *
from app.schemas.role_schema import *
from app.schemas.permission_schema import *
from app.schemas.category_schema import *
from app.schemas.article_schema import *
from app.schemas.article_like_schema import *
from app.schemas.article_comment_schema import *

__all__ = [
    'LoginSchema',
    'RegisterSchema',
    'TokenVOSchema',
    'SysUserFormSchema',
    'SysUserPageQuerySchema',
    'SysRoleFormSchema',
    'SysRolePageQuerySchema',
    'SysPermissionFormSchema',
    'SysPermissionPageQuerySchema',
    'CategoryFormSchema',
    'CategoryPageQuerySchema',
    'ArticleFormSchema',
    'ArticlePageQuerySchema',
    'ArticlePublishSchema',
    'ArticleLikeFormSchema',
    'ArticleCommentFormSchema',
    'ArticleCommentPageQuerySchema',
]
