from inspilot_cloud_baby.auth import CurrentUser
from inspilot_cloud_baby.models import KnowledgeSensitivity, ProjectVisibility
from inspilot_cloud_baby.retrieval import KnowledgeDocument, retrieve_documents


def test_retrieval_filters_invisible_sensitive_documents() -> None:
    user = CurrentUser(user_id="u1", is_company_user=True, project_ids=set())
    docs = [
        KnowledgeDocument(
            id="k1",
            project_id="p1",
            project_visibility=ProjectVisibility.COMPANY_VISIBLE,
            sensitivity=KnowledgeSensitivity.PUBLIC_SUMMARY,
            title="华南车险项目背景",
            body="项目采用跳转模式，适合快速上线。",
        ),
        KnowledgeDocument(
            id="k2",
            project_id="p1",
            project_visibility=ProjectVisibility.COMPANY_VISIBLE,
            sensitivity=KnowledgeSensitivity.SENSITIVE,
            title="华南车险项目费率",
            body="详细费率 2.5%。",
        ),
    ]

    results = retrieve_documents(query="华南 车险 项目", user=user, documents=docs)

    assert [doc.id for doc in results] == ["k1"]


def test_retrieval_scores_matching_documents_first() -> None:
    user = CurrentUser(user_id="u1", is_company_user=True, project_ids={"p1"})
    docs = [
        KnowledgeDocument(
            id="k1",
            project_id="p1",
            project_visibility=ProjectVisibility.PROJECT_MEMBERS,
            sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
            title="系统问题",
            body="按钮不好找。",
        ),
        KnowledgeDocument(
            id="k2",
            project_id="p1",
            project_visibility=ProjectVisibility.PROJECT_MEMBERS,
            sensitivity=KnowledgeSensitivity.PROJECT_RESTRICTED,
            title="直连方案",
            body="直连 API 包含支付回调和出单回调。",
        ),
    ]

    results = retrieve_documents(query="直连 回调", user=user, documents=docs)

    assert [doc.id for doc in results] == ["k2", "k1"]
