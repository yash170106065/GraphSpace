from __future__ import unicode_literals

from applications.users.models import *
from django.conf import settings
from graphspace.mixins import *
import json
from sqlalchemy import ForeignKeyConstraint, text, Enum, Boolean

Base = settings.BASE


# ================== Table Definitions =================== #

class Discussion(IDMixin, TimeStampMixin, Base):
    __tablename__ = 'discussion'

    message = Column(String, nullable=False)
    is_resolved = Column(Integer, nullable=False, default=0)
    description = Column(String, nullable=True)

    owner_email = Column(String, ForeignKey('user.email', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="owned_discussions", uselist=False)

    group_id = Column(Integer, ForeignKey('group.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    group = relationship("Group", back_populates="group_discussions", uselist=False)

    parent_discussion_id = Column(Integer, ForeignKey('discussion.id', ondelete="CASCADE", onupdate="CASCADE"),
                                  nullable=True)
    # groups = association_proxy('discussions_with_groups', 'group')
    constraints = ()
    indices = ()

    @declared_attr
    def __table_args__(cls):
        args = cls.constraints + cls.indices
        return args

    def serialize(cls, **kwargs):
        return {
            'id': cls.id,
            'owner_email': cls.owner_email,
            'message': cls.message,
            'description': cls.description,
            'is_resolved': cls.is_resolved,
            'group_id': cls.group_id,
            'parent_discussion_id': cls.parent_discussion_id,
            'group_owner_email': cls.group.owner_email,
            'created_at': cls.created_at.isoformat(),
            'updated_at': cls.updated_at.isoformat()
        }


# class GroupToDiscussion(TimeStampMixin, Base):
#     __tablename__ = 'group_to_discussion'
#
#     discussion_id = Column(Integer, ForeignKey('discussion.id', ondelete="CASCADE", onupdate="CASCADE"),
#                            primary_key=True)
#     group_id = Column(Integer, ForeignKey('group.id', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
#
#     discussion = relationship("Discussion", backref=backref("discussions_with_groups", cascade="all, delete-orphan"))
#     group = relationship("Group", backref=backref("group_discussions", cascade="all, delete-orphan"))
#
#     indices = (Index('group2discussion_idx_discussion_id_group_id', 'discussion_id', 'group_id'),)
#     constraints = ()
#
#     @declared_attr
#     def __table_args__(cls):
#         args = cls.constraints + cls.indices
#         return args
#
#     def serialize(cls, **kwargs):
#         return {
#             'group_id': cls.group_id,
#             'discussion_id': cls.discussion_id,
#             'created_at': cls.created_at.isoformat(),
#             'updated_at': cls.updated_at.isoformat()
#         }
