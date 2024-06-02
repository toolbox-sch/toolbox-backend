from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.auth.application.service.jwt import JwtService
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.adapter.output.persistence.sqlalchemy.user_file import UserFileSQLAlchemyRepo
from app.user.application.service.user import UserService
from app.user.application.service.user_file import UserFileService


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["app"])

    user_repo = Singleton(UserSQLAlchemyRepo)
    user_repo_adapter = Factory(UserRepositoryAdapter, user_repo=user_repo)
    user_service = Factory(UserService, repository=user_repo_adapter)

    user_file_repo = Singleton(UserFileSQLAlchemyRepo)
    user_file_service = Factory(UserFileService, repository=user_file_repo)

    jwt_service = Factory(JwtService)
