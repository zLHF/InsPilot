import { useMemo, useState } from "react";

const scenarioCopy = {
  knowledge: {
    label: "历史知识",
    icon: "travel_explore",
    prompt: "问历史项目、费率、接口编号、条款来源",
    accent: "fact",
  },
  change: {
    label: "项目变更",
    icon: "sync_alt",
    prompt: "描述原方案、目标方案、影响范围",
    accent: "candidate",
  },
  requirement: {
    label: "需求提炼",
    icon: "schema",
    prompt: "把业务想法整理成产品和研发可消费材料",
    accent: "secondary",
  },
  issue: {
    label: "系统问题",
    icon: "bug_report",
    prompt: "补齐页面、路径、复现步骤和证据",
    accent: "error",
  },
};

const historyItems = [
  {
    type: "项目变更",
    title: "尊享一生2024 - 费率变更",
    status: "已提交",
    meta: "钉钉流程 DREQ-240619 · v3",
    tone: "submitted",
  },
  {
    type: "系统问题",
    title: "移动出单页身份证 OCR 失败",
    status: "待确认",
    meta: "问题已定位，待提交流转 · v1",
    tone: "review",
  },
  {
    type: "历史知识",
    title: "学平险投保接口编号查询",
    status: "已解决",
    meta: "引用 3 条事实层资料 · 2 分钟前",
    tone: "done",
  },
];

function Icon({ children }) {
  return <span className="material-symbols-outlined" aria-hidden="true">{children}</span>;
}

function Header({ submitted }) {
  return (
    <header className="app-header">
      <div className="profile-row">
        <div className="avatar" aria-label="User profile">刘</div>
        <div>
          <p className="eyebrow">钉钉移动工作台</p>
          <h1>InsPilot 云小宝</h1>
        </div>
      </div>
      <div className="header-status">
        <span className="status-pill good"><Icon>verified_user</Icon> PII 脱敏中</span>
        <span className={submitted ? "status-pill good" : "status-pill warn"}>
          <Icon>{submitted ? "task_alt" : "pending_actions"}</Icon>
          {submitted ? "钉钉流程已回传" : "待确认输出"}
        </span>
      </div>
    </header>
  );
}

function ChatTab({
  activeScenario,
  setActiveScenario,
  uploadPanelOpen,
  setUploadPanelOpen,
  outputOpen,
  setOutputOpen,
  submitted,
  setSubmitted,
  maskSensitive,
  setMaskSensitive,
}) {
  const scenario = scenarioCopy[activeScenario];
  const evidenceLabel = maskSensitive ? "张** / 138****2901" : "张晨宇 / 13866772901";

  return (
    <section className="tab-panel chat-panel" aria-label="智能会话主页">
      <div className="hero-card">
        <p className="eyebrow">今日优先保障链路</p>
        <h2>从零散表达，到可流转材料</h2>
        <p>自动识别场景、追问缺口、引用知识来源，并在提交前让业务人员确认。</p>
      </div>

      <div className="scenario-grid" aria-label="场景选择">
        {Object.entries(scenarioCopy).map(([key, item]) => (
          <button
            className={`scenario-card ${activeScenario === key ? "active" : ""} ${item.accent}`}
            key={key}
            onClick={() => setActiveScenario(key)}
            type="button"
          >
            <Icon>{item.icon}</Icon>
            <strong>{item.label}</strong>
            <span>{item.prompt}</span>
          </button>
        ))}
      </div>

      <div className="conversation">
        <div className="message user-message">
          <p>尊享一生 2024 想把缴费期从 10 年改为 15 年，客户说截图里的费率也不一致。</p>
        </div>
        <div className="message bot-message">
          <div className="message-head">
            <span className={`intent-dot ${scenario.accent}`} />
            <strong>识别为：{scenario.label}</strong>
            <span>置信度 0.86</span>
          </div>
          <p>我会先定位历史项目和现行费率，再补齐原方案、目标方案、影响范围和证据来源。</p>
          <div className="progress-card">
            <div><span>项目定位</span><strong>已确认</strong></div>
            <div><span>附件解析</span><strong>排队中</strong></div>
            <div><span>影响范围</span><strong>待补充</strong></div>
          </div>
        </div>

        <div className="output-preview">
          <div className="section-title">
            <div>
              <p className="eyebrow">结构化输出</p>
              <h3>变更单预览</h3>
            </div>
            <button
              aria-label="查看结构化输出"
              type="button"
              onClick={() => setOutputOpen(true)}
            >
              查看
            </button>
          </div>
          <div className="layer-row fact">
            <span>事实层</span>
            <p>当前缴费期 10 年，费率表来源：项目资料 v2024.5</p>
          </div>
          <div className="layer-row candidate">
            <span>候选层</span>
            <p>截图疑似为 2023 旧费率，需知识库管理员审核</p>
          </div>
          <div className="layer-row reference">
            <span>参考层</span>
            <p>引用 PRD §11.2 和项目附件 2 个片段</p>
          </div>
        </div>

        <div className="security-card">
          <div>
            <p className="eyebrow">PII 与权限</p>
            <h3>{evidenceLabel}</h3>
            <p>项目公司内公开，附件和详细费率仍按项目受限资料处理。</p>
          </div>
          <button type="button" onClick={() => setMaskSensitive(!maskSensitive)}>
            {maskSensitive ? "申请授权查看" : "恢复脱敏视图"}
          </button>
        </div>
      </div>

      {uploadPanelOpen && (
        <div className="upload-panel" aria-label="多模态上传面板">
          {[
            ["mic", "语音", "60 秒内转写"],
            ["image", "截图", "OCR/VLM 解析"],
            ["attach_file", "文件", "进入知识投喂"],
            ["videocam", "录屏", "异步处理"],
          ].map(([icon, title, desc]) => (
            <button key={title} type="button">
              <Icon>{icon}</Icon>
              <strong>{title}</strong>
              <span>{desc}</span>
            </button>
          ))}
          <p>今日视频配额剩余 14 分钟；图片识别剩余 186 张。</p>
        </div>
      )}

      <div className="composer">
        <button
          aria-label="打开多模态上传"
          className="icon-button"
          onClick={() => setUploadPanelOpen(!uploadPanelOpen)}
          type="button"
        >
          <Icon>add_circle</Icon>
        </button>
        <input aria-label="输入消息" placeholder={scenario.prompt} />
        <button className="send-button" type="button" onClick={() => setOutputOpen(true)}>
          <Icon>arrow_upward</Icon>
        </button>
      </div>

      {outputOpen && (
        <div className="drawer-backdrop" role="dialog" aria-modal="true" aria-label="结构化输出抽屉">
          <div className="output-drawer">
            <div className="drawer-head">
              <div>
                <p className="eyebrow">Markdown / JSON</p>
                <h2>结构化输出确认</h2>
              </div>
              <button aria-label="关闭" className="icon-button" onClick={() => setOutputOpen(false)} type="button">
                <Icon>close</Icon>
              </button>
            </div>
            <div className="schema-card">
              <code>{"{ output_type: 'change_request', output_version: 3 }"}</code>
              <p>并发提交使用 output_version 乐观锁，退回补充会生成新版本。</p>
            </div>
            <ul className="check-list">
              <li><Icon>check_circle</Icon> 原方案、目标方案、影响范围已补齐</li>
              <li><Icon>check_circle</Icon> 关键字段均有来源引用</li>
              <li><Icon>warning</Icon> 候选费率仍需人工审核</li>
            </ul>
            <button
              className="primary-action"
              onClick={() => {
                setSubmitted(true);
                setOutputOpen(false);
              }}
              type="button"
            >
              提交钉钉流程
            </button>
          </div>
        </div>
      )}
    </section>
  );
}

function HistoryTab({ submitted }) {
  const items = useMemo(() => {
    if (!submitted) return historyItems;
    return [
      {
        type: "项目变更",
        title: "尊享一生2024 - 缴费期调整",
        status: "已提交",
        meta: "钉钉流程 DREQ-240621 · 刚刚回传",
        tone: "submitted",
      },
      ...historyItems,
    ];
  }, [submitted]);

  return (
    <section className="tab-panel history-panel" aria-label="记录">
      <div className="page-title">
        <p className="eyebrow">记录</p>
        <h2>会话与流转追溯</h2>
      </div>
      <label className="search-box">
        <Icon>search</Icon>
        <input placeholder="搜索项目名或内容关键字" />
      </label>
      <div className="filter-row">
        {["全部", "待补充", "待确认", "已提交", "已解决"].map((item) => (
          <button className={item === "全部" ? "active" : ""} key={item} type="button">{item}</button>
        ))}
      </div>
      <div className="history-list">
        {items.map((item) => (
          <article className="history-card" key={`${item.title}-${item.meta}`}>
            <div>
              <span className={`type-chip ${item.tone}`}>{item.type}</span>
              <h3>{item.title}</h3>
              <p>{item.meta}</p>
            </div>
            <strong>{item.status}</strong>
          </article>
        ))}
      </div>
    </section>
  );
}

function ProfileTab({ maskSensitive, setMaskSensitive }) {
  return (
    <section className="tab-panel profile-panel" aria-label="我的">
      <div className="profile-card">
        <div className="avatar large" aria-label="User profile">刘</div>
        <div>
          <p className="eyebrow">市场业务代表</p>
          <h2>刘航飞</h2>
          <p>华南业务线 · 8 个项目可见</p>
        </div>
      </div>
      <div className="metric-grid">
        <div><strong>42</strong><span>知识贡献</span></div>
        <div><strong>96%</strong><span>输出可追溯</span></div>
        <div><strong>3</strong><span>待补充事项</span></div>
      </div>
      <div className="settings-list">
        <button type="button" onClick={() => setMaskSensitive(!maskSensitive)}>
          <Icon>shield_lock</Icon>
          <span>PII 脱敏设置</span>
          <strong>{maskSensitive ? "脱敏视图" : "授权查看"}</strong>
        </button>
        <button type="button">
          <Icon>key</Icon>
          <span>数据权限申请</span>
          <strong>需审计</strong>
        </button>
        <button type="button">
          <Icon>library_add</Icon>
          <span>知识库维护</span>
          <strong>轻量投喂</strong>
        </button>
      </div>
      <div className="permission-card">
        <p className="eyebrow">项目开放级别</p>
        <h3>公司内公开 + 项目受限资料</h3>
        <p>公开项目只开放脱敏摘要和复用经验；合同、截图、详细费率、接口配置和 PII 仍需要项目成员或授权。</p>
      </div>
    </section>
  );
}

function TabBar({ activeTab, setActiveTab }) {
  const tabs = [
    ["chat", "对话", "chat"],
    ["history", "记录", "history"],
    ["profile", "我的", "person"],
  ];

  return (
    <nav className="tab-bar" aria-label="主导航">
      {tabs.map(([key, label, icon]) => (
        <button
          className={activeTab === key ? "active" : ""}
          key={key}
          onClick={() => setActiveTab(key)}
          type="button"
        >
          <Icon>{icon}</Icon>
          <span>{label}</span>
        </button>
      ))}
    </nav>
  );
}

export function App() {
  const [activeTab, setActiveTab] = useState("chat");
  const [activeScenario, setActiveScenario] = useState("change");
  const [uploadPanelOpen, setUploadPanelOpen] = useState(false);
  const [outputOpen, setOutputOpen] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [maskSensitive, setMaskSensitive] = useState(true);

  return (
    <main className="prototype-stage">
      <div className="phone-shell">
        <Header submitted={submitted} />
        <div className="screen-scroll">
          {activeTab === "chat" && (
            <ChatTab
              activeScenario={activeScenario}
              setActiveScenario={setActiveScenario}
              uploadPanelOpen={uploadPanelOpen}
              setUploadPanelOpen={setUploadPanelOpen}
              outputOpen={outputOpen}
              setOutputOpen={setOutputOpen}
              submitted={submitted}
              setSubmitted={setSubmitted}
              maskSensitive={maskSensitive}
              setMaskSensitive={setMaskSensitive}
            />
          )}
          {activeTab === "history" && <HistoryTab submitted={submitted} />}
          {activeTab === "profile" && (
            <ProfileTab maskSensitive={maskSensitive} setMaskSensitive={setMaskSensitive} />
          )}
        </div>
        <TabBar activeTab={activeTab} setActiveTab={setActiveTab} />
      </div>
    </main>
  );
}
