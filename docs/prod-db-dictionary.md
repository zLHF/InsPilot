# InsPilot 生产数据库字典 (YDB_GeneralSystemDB)

> SQL Server 数据库。本文件由数据字典 HTML 自动生成，供 NL2SQL 使用。
> 共 436 张表。如生产库结构变更，重新生成此文件。

---

## 目录

- [T_Enterprise_AuditLog](#t_enterprise_auditlog)
- [T_BrokerCompany_Info](#t_brokercompany_info) — 经纪公司表
- [T_changjiang_interface](#t_changjiang_interface)
- [T_PProduct_Enclosure](#t_pproduct_enclosure)
- [T_PProduct_GuaranteeExtend](#t_pproduct_guaranteeextend) — 履约订单表扩展
- [T_XK_RebateInfo](#t_xk_rebateinfo) — 返点信息表（主表）
- [T_PProduct_ServeRiskResAttachment](#t_pproduct_serveriskresattachment) — 风险附件表
- [T_Enterprise_AuthActionRecord](#t_enterprise_authactionrecord)
- [T_XK_RebateBatch](#t_xk_rebatebatch)
- [t_toubaoNo_invalid](#t_toubaono_invalid) — 投标编码失效表
- [T_NJDT_User](#t_njdt_user)
- [T_GzZrx_DataPermissions](#t_gzzrx_datapermissions) — 雇主责任险-数据权限表
- [T_PProduct_ServeTemplate](#t_pproduct_servetemplate) — 多险种服务模板
- [T_GzZrx_GuaranteeEmployee](#t_gzzrx_guaranteeemployee) — 雇主责任险--参保雇员信息
- [T_MobileMsg_Dict](#t_mobilemsg_dict)
- [T_Enterprise_AuthAttachment](#t_enterprise_authattachment)
- [T_tsign_Authentication](#t_tsign_authentication)
- [T_PProduct_EnterpriseAccount](#t_pproduct_enterpriseaccount) — 企业子账号信息表
- [T_XK_Order](#t_xk_order) — 线客订单表
- [T_OnlineInvoice_User](#t_onlineinvoice_user) — 线上开票-用户表
- [T_PProduct_ServeTemplateServeDetail](#t_pproduct_servetemplateservedetail) — 模板服务项明细
- [T_XK_Platform](#t_xk_platform) — 线客平台表
- [T_tsign_Evidence](#t_tsign_evidence)
- [T_NJDT_Role](#t_njdt_role)
- [T_ZX_UserEnterprise](#t_zx_userenterprise) — 振鑫小程序-用户企业关联表
- [T_GzZrx_Channel](#t_gzzrx_channel) — 雇主责任险一级渠道表
- [T_PProductYz_Cliam](#t_pproductyz_cliam) — 医责险-理赔
- [T_PProduct_EnterpriseAttachment](#t_pproduct_enterpriseattachment) — 农民工履约企业附件表
- [T_tsign_Guarantee](#t_tsign_guarantee)
- [T_PProduct_SettleInfo](#t_pproduct_settleinfo) — 履约理赔申请资料表
- [T_Esign_UserDataAccess](#t_esign_userdataaccess) — 签章管理员设置
- [T_Enterprise_RemarkLog](#t_enterprise_remarklog)
- [T_PProduct_ExecutePolicyInfo](#t_pproduct_executepolicyinfo)
- [T_MobileMsg_ChannelSign](#t_mobilemsg_channelsign)
- [T_PayLog_Manual](#t_paylog_manual) — 模拟支付记录信息表
- [T_tsign_NSH](#t_tsign_nsh)
- [T_PProduct_SuperviseMode](#t_pproduct_supervisemode)
- [T_EnterpriseDiscount_CardID](#t_enterprisediscount_cardid)
- [T_PProduct_Files](#t_pproduct_files)
- [T_tsign_PayLog](#t_tsign_paylog) — 支付记录表
- [T_PProduct_SupervisePRC](#t_pproduct_superviseprc)
- [T_EnterpriseDiscount_ImportLog](#t_enterprisediscount_importlog)
- [T_tsign_Seal](#t_tsign_seal)
- [T_NJDT_RoleMenu](#t_njdt_rolemenu)
- [T_PProduct_FilesUrl](#t_pproduct_filesurl)
- [T_MobileMsg_BatchLog](#t_mobilemsg_batchlog)
- [T_tsign_SceneDataDictionary](#t_tsign_scenedatadictionary)
- [T_OnlineInvoice_InvoiceInfo](#t_onlineinvoice_invoiceinfo) — 发票信息表
- [T_PProduct_SupervisePRCEnInsurance](#t_pproduct_superviseprceninsurance)
- [T_EnterpriseDiscount_Info](#t_enterprisediscount_info)
- [T_ZX_Banner](#t_zx_banner) — 振金Banner表
- [T_Project_UpdateLog](#t_project_updatelog) — 项目工程更新日志表
- [T_PProductYz_CliamTPRecord](#t_pproductyz_cliamtprecord) — 理赔摊赔记录
- [T_OnlineInvoice_UserEntVerify](#t_onlineinvoice_userentverify) — 线上发票-企业认证记录表
- [T_Org_PushInfo](#t_org_pushinfo) — 经纪机构数据推送配置表
- [T_PProduct_SupervisePRCEnInsuranceInsurance](#t_pproduct_superviseprceninsuranceinsurance)
- [T_EnterpriseDiscount_Log](#t_enterprisediscount_log)
- [T_tsign_updateLog](#t_tsign_updatelog)
- [T_PProduct_GuaranteeCargoStandardList](#t_pproduct_guaranteecargostandardlist)
- [T_PRC_ApiUrl](#t_prc_apiurl)
- [T_VoiceNotice_Task](#t_voicenotice_task)
- [T_PProduct_SupervisePRCRelation](#t_pproduct_superviseprcrelation)
- [T_ZX_PrizeRecord](#t_zx_prizerecord) — 振鑫-奖品记录表
- [T_Epoint_Guarantee_tb](#t_epoint_guarantee_tb)
- [T_PProductYz_UserPRCEnInsurance](#t_pproductyz_userprceninsurance)
- [T_PProduct_GuaranteeDelayRecord](#t_pproduct_guaranteedelayrecord) — 保单延期记录
- [T_PProductWarn_Insurance](#t_pproductwarn_insurance) — 农民工工资支付监控平台-金融机构基本信息
- [T_OnlineInvoice_QueryEntParam](#t_onlineinvoice_queryentparam) — 用户有效检索参数
- [T_zk_interface](#t_zk_interface)
- [T_VoiceNotice_TaskLog](#t_voicenotice_tasklog)
- [T_PProduct_SuperviseRule](#t_pproduct_superviserule)
- [T_Epoint_Interface](#t_epoint_interface)
- [T_XK_Contacts_DataStatisticsRule](#t_xk_contacts_datastatisticsrule) — 线客联系人出单数据监测规则表
- [T_GzZrx_DataPermissionsPRC](#t_gzzrx_datapermissionsprc) — 雇主责任险-数据权限与二级渠道关系表
- [T_Pay_Log](#t_pay_log) — 支付记录表
- [T_PProduct_GuaranteeDelayRecordApply](#t_pproduct_guaranteedelayrecordapply)
- [T_ZX_EquityCouponGroup](#t_zx_equitycoupongroup) — 权益优惠券组表
- [T_VoiceNotice_TaskPhone](#t_voicenotice_taskphone)
- [T_PProduct_Surrender](#t_pproduct_surrender) — 履约申请退保、关闭订单记录
- [T_Epoint_InterfaceExtend](#t_epoint_interfaceextend)
- [T_ZX_Channel](#t_zx_channel)
- [T_Relation_PRCEnInsuranceUserAcct](#t_relation_prceninsuranceuseracct) — 易联请求参数设置表
- [T_PProduct_GuaranteeEditLog](#t_pproduct_guaranteeeditlog) — 编辑订单字段信息记录表
- [T_PProduct_Guarantee_Protocol](#t_pproduct_guarantee_protocol) — 商城增信-协议表
- [T_VoiceNotice_TaskPhoneVariable](#t_voicenotice_taskphonevariable)
- [T_PProduct_tsignAuthentication](#t_pproduct_tsignauthentication)
- [T_PProduct_GuaranteeEnAttachment](#t_pproduct_guaranteeenattachment) — 农民工履约保单附件表
- [T_ExportTemplate_Log](#t_exporttemplate_log) — 运维导出历史记录表
- [T_ZX_PrizeConfigs](#t_zx_prizeconfigs) — 振鑫-奖品配置表
- [T_PProduct_PRCEnInsuranceBusiManager](#t_pproduct_prceninsurancebusimanager) — 客户经理信息表
- [T_GzZrx_GuaranteeMain](#t_gzzrx_guaranteemain) — 主订单表
- [T_VoiceNotice_Template](#t_voicenotice_template)
- [T_PProduct_UserProduct](#t_pproduct_userproduct) — 农民工履约企业所属产品表
- [T_Fstate_Order](#t_fstate_order)
- [T_WeekDay_Cache](#t_weekday_cache)
- [T_PProductYZ_PRCEnInsurance](#t_pproductyz_prceninsurance)
- [T_PProduct_GuaranteeInsDetail](#t_pproduct_guaranteeinsdetail) — 订单保险明细
- [T_Enterprise_Mac](#t_enterprise_mac)
- [T_PProduct_SXPushIndex](#t_pproduct_sxpushindex) — 推送次数记录表，生成工资保证金账户收支编号用到
- [T_Guarantee_AuditLog](#t_guarantee_auditlog) — 人工审核保单日志
- [T_GzZrx_InvoiceLog](#t_gzzrx_invoicelog) — 雇主责任险--发票申请记录表
- [T_GzZrx_InsuranceInfo](#t_gzzrx_insuranceinfo) — 雇主责任险-金融机构表
- [T_Enterprise_BlackLog](#t_enterprise_blacklog) — 黑名单拦截记录表
- [T_zijin_interface](#t_zijin_interface)
- [T_PProductYz_Coinsurant](#t_pproductyz_coinsurant)
- [T_PProduct_GuaranteeLaborUnit](#t_pproduct_guaranteelaborunit)
- [T_Guarantee_Cancel](#t_guarantee_cancel) — 保单申请撤销表
- [T_ZX_PointsUser](#t_zx_pointsuser) — 担保小程序-积分用户表
- [VerificationCode](#verificationcode)
- [T_NJDT_PrcChannel](#t_njdt_prcchannel)
- [T_ZX_GuaranteeBatch](#t_zx_guaranteebatch) — 振鑫小程序-投标批次表
- [T_GzZrx_PRC](#t_gzzrx_prc) — 二级渠道表
- [T_GzZrx_BaseFile](#t_gzzrx_basefile)
- [T_PProductYz_CoinsurantLink](#t_pproductyz_coinsurantlink)
- [T_PProduct_GuaranteeProjectPayList](#t_pproduct_guaranteeprojectpaylist)
- [T_PProduct_InsuranceInfo](#t_pproduct_insuranceinfo) — 多险种保险公司表
- [T_NJDT_PRCShowInfo](#t_njdt_prcshowinfo)
- [T_ChannelOrder_ChannelInfo](#t_channelorder_channelinfo) — 渠道信息
- [T_PProductYz_Enclosure](#t_pproductyz_enclosure) — 医责险-附件模板类型
- [T_PProduct_GuaranteeService](#t_pproduct_guaranteeservice) — 农民工延时赔付
- [T_Guarantee_DataBak](#t_guarantee_databak)
- [T_Epoint_PushGuaranteeLog](#t_epoint_pushguaranteelog)
- [T_Base_Area_ZY_cw](#t_base_area_zy_cw)
- [T_Guarantee_Info_yx](#t_guarantee_info_yx) — 投保单信息表
- [T_XK_RebateDetail](#t_xk_rebatedetail) — 返点申请明细
- [T_PProduct_GuaranteeServiceFiles](#t_pproduct_guaranteeservicefiles) — 农民工延时赔付凭证附件表
- [T_ZX_PrizeRecord_Order](#t_zx_prizerecord_order)
- [T_NJDT_Menus](#t_njdt_menus)
- [T_GzZrx_InsuranceFileTemplateBase](#t_gzzrx_insurancefiletemplatebase)
- [T_Guarantee_MonthData](#t_guarantee_monthdata) — 月份报表数据表
- [T_GzZrx_Menus](#t_gzzrx_menus) — 雇主责任险-用户公共菜单表
- [T_XK_RebateBatchRelation](#t_xk_rebatebatchrelation)
- [T_PProductYz_MedicalAccident](#t_pproductyz_medicalaccident) — 医责险-事故信息表
- [T_PProduct_GuaranteeServiceLog](#t_pproduct_guaranteeservicelog)
- [T_XK_RebateInfoCode](#t_xk_rebateinfocode)
- [T_ChannelOrder_OrderInfo](#t_channelorder_orderinfo) — 订单
- [T_ZX_PrizeCount](#t_zx_prizecount) — 振鑫-活动次数
- [T_SysOperation_Log](#t_sysoperation_log)
- [T_XK_DictType](#t_xk_dicttype) — 线客字典类型表
- [T_PProductYz_Menus](#t_pproductyz_menus)
- [T_PProduct_InsDetailInfo](#t_pproduct_insdetailinfo) — 保险信息明细信息
- [T_Enterprise_SendMoney](#t_enterprise_sendmoney) — 企业打款认证记录表
- [T_GzZrx_Guarantee](#t_gzzrx_guarantee) — 雇主责任险--订单表
- [T_PProductYz_SetShowRecord](#t_pproductyz_setshowrecord)
- [T_Base_Area_ZY_cxp](#t_base_area_zy_cxp)
- [T_Guarantee_Source](#t_guarantee_source)
- [T_ZX_ProductInfo](#t_zx_productinfo) — 标后产品表
- [T_NJDT_ChannelCode](#t_njdt_channelcode) — 渠道编码生产规则记录表
- [T_PProductYz_Organ](#t_pproductyz_organ)
- [T_PProduct_InsDetailSelectInfo](#t_pproduct_insdetailselectinfo)
- [T_GzZrx_InsuranceFileTemplate](#t_gzzrx_insurancefiletemplate)
- [T_GzZrx_OperationLog](#t_gzzrx_operationlog) — 雇主货运险-操作日志表
- [T_ZX_GoodsInfo](#t_zx_goodsinfo) — 振鑫小程序-商品信息表
- [T_Guarantee_Surrender](#t_guarantee_surrender)
- [T_NJDT_Channel](#t_njdt_channel) — 渠道信息表
- [T_PProduct_EnterpriseSendMoney](#t_pproduct_enterprisesendmoney)
- [T_ZX_PointsType](#t_zx_pointstype) — 担保小程序-积分类型表
- [T_PProduct_InsItemInfo](#t_pproduct_insiteminfo) — 保险信息分类信息
- [T_Base_Area_ZY](#t_base_area_zy)
- [K_ToolUser](#k_tooluser)
- [T_ZX_PrizeCountRecord](#t_zx_prizecountrecord) — 振鑫-活动次数发放记录
- [T_Base_Area_ZY_old](#t_base_area_zy_old) — 行政区划编码表
- [T_ZX_Equity](#t_zx_equity) — 权益表
- [T_XK_Dict](#t_xk_dict) — 线客字典详情表
- [T_PProductYz_PRCEnclosure](#t_pproductyz_prcenclosure) — 医责险-渠道附件模板
- [T_PProduct_InsProgramme](#t_pproduct_insprogramme) — 保险方案
- [T_PProductYz_PRCEnclosureGuarantee](#t_pproductyz_prcenclosureguarantee) — 医责险-事故附件上传
- [T_PProduct_Insurance](#t_pproduct_insurance) — 农民工险种列表
- [T_Enterprise_Info](#t_enterprise_info) — 企业信息表
- [T_GzZrx_PRCInsurance](#t_gzzrx_prcinsurance) — 承保机构表
- [T_Invoice_Log](#t_invoice_log) — 发票申请记录表
- [T_Base_Area_CT](#t_base_area_ct) — 行政区划编码表
- [T_ZX_ProductPartners](#t_zx_productpartners)
- [T_PProduct_Attachment](#t_pproduct_attachment)
- [YanShiTemp](#yanshitemp)
- [T_Insurance_FileTemplate](#t_insurance_filetemplate)
- [T_GzZrx_Enterprise](#t_gzzrx_enterprise)
- [T_PProductYz_Result](#t_pproductyz_result) — 医责险-确责记录
- [T_NJDT_ShowInfoTemplate](#t_njdt_showinfotemplate)
- [T_PProduct_ProductInfo](#t_pproduct_productinfo) — 农民工项目表
- [T_PProduct_IntegratedPRCAttachment](#t_pproduct_integratedprcattachment)
- [T_Insurance_FileTemplateBase](#t_insurance_filetemplatebase)
- [T_ZX_UserEnEquity](#t_zx_userenequity) — 用户和权益关联表
- [T_Policy_FreeIDs](#t_policy_freeids) — 后台人工去限制出单ID记录表，比如联银
- [T_PaymentSystem_Insurance](#t_paymentsystem_insurance)
- [T_PProductYz_RoleMenus](#t_pproductyz_rolemenus)
- [T_PProduct_ConstructionGrade](#t_pproduct_constructiongrade)
- [T_PProduct_IntegratedCommodity](#t_pproduct_integratedcommodity)
- [T_Insurance_InfoDoSign](#t_insurance_infodosign)
- [T_GzZrx_InsuranceFile](#t_gzzrx_insurancefile)
- [T_ZX_ProductInquiryExtend](#t_zx_productinquiryextend)
- [T_Invoice_Info](#t_invoice_info) — 发票信息表
- [T_Insurance_Info](#t_insurance_info)
- [T_PProductYz_Roles](#t_pproductyz_roles)
- [T_Base_Nature](#t_base_nature)
- [T_GzZrx_interface](#t_gzzrx_interface)
- [T_PProductYz_OperationLog](#t_pproductyz_operationlog) — 医责险操作记录
- [T_PProduct_IntegratedCommodityLink](#t_pproduct_integratedcommoditylink)
- [T_Esign_Apply](#t_esign_apply)
- [T_ZX_ChannelLeveltwo](#t_zx_channelleveltwo)
- [T_ZX_GoodsType](#t_zx_goodstype) — 振鑫小程序-商品类别表
- [T_Login_Black](#t_login_black) — 登陆黑名单表
- [T_Project_Info](#t_project_info) — 项目信息表
- [T_Epoint_PlatformConfig](#t_epoint_platformconfig)
- [T_GzZrx_PayLog](#t_gzzrx_paylog) — 雇主责任险--支付记录表
- [T_PProductYz_UserDataAccess](#t_pproductyz_userdataaccess) — 数据权限角色
- [T_PRC_TypeModeSetting](#t_prc_typemodesetting)
- [T_ZX_UserLoginLog](#t_zx_userloginlog) — 振鑫小程序用户登录表
- [T_QuitGuarantee_AuditLogFile](#t_quitguarantee_auditlogfile) — 退保推送文件日志表
- [T_QuitGuarantee_PRCEnInsuranceEnAttachment](#t_quitguarantee_prceninsuranceenattachment)
- [T_PProduct_IntegratedPRC](#t_pproduct_integratedprc)
- [T_Enterprise_Attachment](#t_enterprise_attachment) — 企业附件表
- [T_Login_Log](#t_login_log) — 登陆日志表
- [T_PProductYz_UserDataAccess_Coinsurant](#t_pproductyz_userdataaccess_coinsurant)
- [T_PProduct_IntegratedProduct](#t_pproduct_integratedproduct)
- [T_ZX_GoodsImg](#t_zx_goodsimg) — 振鑫小程序-商品信息详情图表
- [T_MobileMsg_Blacklist](#t_mobilemsg_blacklist) — 短信黑名单
- [T_XK_RebateDetail_Apply](#t_xk_rebatedetail_apply) — 返点退回申请
- [T_PProductYz_UserDataAccess_Organ](#t_pproductyz_userdataaccess_organ) — 数据权限角色详情
- [T_PProduct_IntegratedRule](#t_pproduct_integratedrule)
- [T_ZX_EquityCouponGroupEnCoupon](#t_zx_equitycoupongroupencoupon)
- [T_MobileMsg_Log](#t_mobilemsg_log) — 短信发送日志
- [T_Epoint_Guarantee](#t_epoint_guarantee)
- [T_PRC_InterfaceLimit](#t_prc_interfacelimit)
- [T_PProductYz_UserDataAccess_PRC](#t_pproductyz_userdataaccess_prc)
- [T_PProduct_InvoiceInfo](#t_pproduct_invoiceinfo) — 履约企业发票信息表
- [T_Esign_ApplyDetail](#t_esign_applydetail) — 签章文件列表
- [T_MobileMsg_Tel](#t_mobilemsg_tel)
- [T_GzZrx_PaymentVouchers](#t_gzzrx_paymentvouchers) — 雇主责任险-上传凭证记录
- [T_ZX_ConstructionGrade](#t_zx_constructiongrade)
- [T_PProductYz_UserRoles](#t_pproductyz_userroles)
- [T_Guarantee_Project](#t_guarantee_project)
- [T_PProduct_Enterprise](#t_pproduct_enterprise) — 农民工履约企业表
- [T_Esign_ApplyDetail_Signs](#t_esign_applydetail_signs) — 签章步骤
- [T_News_Cla](#t_news_cla) — 新闻帮助类别表
- [T_Epoint_PushGuarantee](#t_epoint_pushguarantee)
- [T_PProductYz_Users](#t_pproductyz_users)
- [T_PProduct_Log](#t_pproduct_log) — 农民工操作日志表
- [T_Host_Redirect](#t_host_redirect)
- [T_News_Info](#t_news_info) — 新闻帮助信息表
- [T_PProduct_PushTimeLog](#t_pproduct_pushtimelog)
- [T_PProduct_Manual](#t_pproduct_manual)
- [T_Epoint_BaseAccountLog](#t_epoint_baseaccountlog)
- [T_OFD_Interface](#t_ofd_interface) — OFD接口配置表
- [T_Esign_SignRecord](#t_esign_signrecord) — 签章记录
- [T_PaymentSystem_PlatformBusiness](#t_paymentsystem_platformbusiness)
- [T_ZX_PointsInfo](#t_zx_pointsinfo) — 担保小程序-积分记录表
- [T_GzZrx_Insurance](#t_gzzrx_insurance) — 雇主责任险-险种表
- [T_PRC_TypeMode](#t_prc_typemode)
- [T_PProduct_OfflineInsuranceInfo](#t_pproduct_offlineinsuranceinfo)
- [T_Offline_Manager](#t_offline_manager)
- [T_XK_Contacts_DataStatisticsExtend](#t_xk_contacts_datastatisticsextend) — 线客联系人出单数据监测预警状态表
- [T_Relation_PRCEnInsurance](#t_relation_prceninsurance)
- [T_Project_Apply](#t_project_apply)
- [T_PProduct_PayLog](#t_pproduct_paylog) — 支付记录表
- [T_Guarantee_InterfaceTransNos](#t_guarantee_interfacetransnos)
- [T_Account_Info](#t_account_info)
- [T_Guarantee_BidInfo](#t_guarantee_bidinfo) — 订单标段表
- [T_OfflineOperationLog](#t_offlineoperationlog) — 线下操作日志表
- [T_Project_DelayLog](#t_project_delaylog)
- [T_ZX_ProductInquiryClaim](#t_zx_productinquiryclaim)
- [T_PProduct_PaymentVouchers](#t_pproduct_paymentvouchers) — 上传凭证记录
- [T_AliAuthorizeSecurity_Records](#t_aliauthorizesecurity_records)
- [T_PProduct_CheckLog](#t_pproduct_checklog) — 多险种初审复核记录
- [T_GzZrx_UserMoenyRecord](#t_gzzrx_usermoenyrecord) — 雇主责任险-用户资金记录表
- [T_Project_FixLog](#t_project_fixlog) — 项目特殊维护记录
- [T_Epoint_PushGuaranteeImportLog](#t_epoint_pushguaranteeimportlog)
- [T_PProduct_Policy](#t_pproduct_policy) — 多险种保单凭证记录列表
- [T_AliPay](#t_alipay)
- [T_pay_log_cardType](#t_pay_log_cardtype)
- [T_Guarantee_InsurancePayLog](#t_guarantee_insurancepaylog) — 保司机构回调支付信息表
- [T_PProduct_PRC](#t_pproduct_prc) — 履约平台类型
- [T_Bank_Flow](#t_bank_flow)
- [T_Pay_Log_ImportLog](#t_pay_log_importlog) — 工行支付导入日志表
- [T_Enterprise_Data](#t_enterprise_data) — 企业库表
- [T_Project_InfoExtension](#t_project_infoextension) — 项目拓展信息表
- [T_Bank_FlowRelation](#t_bank_flowrelation)
- [T_ZX_ProductInquiryQuit](#t_zx_productinquiryquit)
- [T_Pay_Log_LiShui](#t_pay_log_lishui) — 支付记录表
- [T_ProJect_Result](#t_project_result)
- [T_PProduct_PRCEnInsuranceEnclosure](#t_pproduct_prceninsuranceenclosure)
- [T_Bank_Info](#t_bank_info)
- [T_Pay_NoUsed](#t_pay_noused) — 金华支付记录未使用
- [sysdiagrams](#sysdiagrams) — 1
- [T_Project_UpdateField](#t_project_updatefield)
- [T_Bank_OutsidePlatform](#t_bank_outsideplatform)
- [T_GzZrx_QuitInfo](#t_gzzrx_quitinfo) — 雇主-退保信息表
- [T_PayLog_AuditLog](#t_paylog_auditlog)
- [T_PProduct_PRCEnInsuranceEngagedesc](#t_pproduct_prceninsuranceengagedesc)
- [T_PProductYz_PRC](#t_pproductyz_prc)
- [T_Bank_PayLog](#t_bank_paylog)
- [T_ZX_ProductInquiry](#t_zx_productinquiry) — 振鑫产品询价表
- [T_Payment_Vouchers](#t_payment_vouchers) — 上传凭证记录
- [T_GzZrx_ExportList](#t_gzzrx_exportlist) — 导出记录列表
- [T_Coupon_WriteOffLog](#t_coupon_writeofflog) — 优惠券核销记录
- [T_Coupon_Type](#t_coupon_type) — 优惠券类型表
- [T_Push_Log](#t_push_log) — 项目推送获取日志表
- [T_PProduct_ApplyRemind](#t_pproduct_applyremind) — 多险种-业务申请提醒信息表
- [T_PProduct_PRCEnInsuranceRegulator](#t_pproduct_prceninsuranceregulator)
- [T_Base_Area](#t_base_area) — 行政区划编码表
- [T_PaymentSystem_Cancel](#t_paymentsystem_cancel) — 退保记录表
- [T_QuitGuarantee_Attachment](#t_quitguarantee_attachment)
- [T_GzZrx_GLG](#t_gzzrx_glg) — 公路港信息
- [T_PProduct_PRCEnInsuranceTmpContent](#t_pproduct_prceninsurancetmpcontent)
- [T_Insurance_File](#t_insurance_file)
- [T_Base_File](#t_base_file)
- [T_PaymentSystem_CancelLog](#t_paymentsystem_cancellog)
- [T_PProduct_PRCIns](#t_pproduct_prcins) — 渠道险种关联表
- [T_PProduct_ExportStatisticalRecord](#t_pproduct_exportstatisticalrecord)
- [T_Guarantee_extend](#t_guarantee_extend)
- [T_QuitGuarantee_AuditLog](#t_quitguarantee_auditlog)
- [T_Guarantee_Info](#t_guarantee_info) — 投保单信息表
- [T_PProductYz_Guarantee](#t_pproductyz_guarantee) — 医责险-保单表
- [T_PaymentSystem_Enterprise](#t_paymentsystem_enterprise)
- [T_XK_Contacts](#t_xk_contacts) — 线客联系人表
- [T_PProduct_Guarantee](#t_pproduct_guarantee) — 农民工履约保单表
- [T_PProduct_InvoiceLog](#t_pproduct_invoicelog) — 农民工履约保函发票表
- [T_PProduct_ProductCompany](#t_pproduct_productcompany) — 项目三方责任人信息
- [T_Base_PostCode](#t_base_postcode) — 地区邮编表
- [T_QuitGuarantee_GuaranteeAttachment](#t_quitguarantee_guaranteeattachment)
- [T_PaymentSystem_Guarantee](#t_paymentsystem_guarantee)
- [T_GzZrx_PRCInsType](#t_gzzrx_prcinstype) — 雇主责任险--二级渠道和险种关联表
- [T_OnlineInvoice_QueryLog](#t_onlineinvoice_querylog)
- [T_Base_User](#t_base_user) — 投保联系人信息表
- [T_QuitGuarantee_Manual](#t_quitguarantee_manual)
- [T_GzZrx_Users](#t_gzzrx_users) — 雇主责任险-用户表
- [T_PaymentSystem_PayLog](#t_paymentsystem_paylog) — 支付记录表
- [T_GzZrx_InvoiceInfo](#t_gzzrx_invoiceinfo) — 履约企业发票信息表
- [T_PProduct_ProductInfoExtend](#t_pproduct_productinfoextend) — 农民工项目扩展表
- [T_Black_WuXi](#t_black_wuxi) — 无锡投保黑名单
- [T_Pay_Log_Interface](#t_pay_log_interface)
- [T_PaymentSystem_Platform](#t_paymentsystem_platform)
- [T_PProduct_ProductSecurityOfficer](#t_pproduct_productsecurityofficer) — 安全员信息
- [T_Ca_Log](#t_ca_log) — CA登录日志表
- [T_QuotaProject](#t_quotaproject)
- [T_PaymentSystem_Vouchers](#t_paymentsystem_vouchers)
- [T_PProduct_Programme](#t_pproduct_programme)
- [T_CA_Parameter](#t_ca_parameter)
- [T_PProduct_Admin](#t_pproduct_admin) — 农民工管理账号
- [T_Enterprise_Black](#t_enterprise_black) — 黑名单拦截企业表
- [T_Region](#t_region)
- [T_GzZrx_Roles](#t_gzzrx_roles) — 雇主责任险-角色表
- [T_DaPingMu_Log](#t_dapingmu_log) — 大屏幕日志
- [T_CoInsurance_EmailInfo](#t_coinsurance_emailinfo)
- [T_pay_log_discount](#t_pay_log_discount)
- [T_Relation_GuaranteeEnAttachment](#t_relation_guaranteeenattachment) — 投保单和企业附件关联表
- [T_PProduct_Agreement](#t_pproduct_agreement) — 多险种合同表
- [T_GzZrx_PRCInsuranceEngagedesc](#t_gzzrx_prcinsuranceengagedesc) — 雇主责任险-特约配置
- [T_ZX_User](#t_zx_user) — 振鑫小程序用户表
- [T_PProduct_QualificationRate](#t_pproduct_qualificationrate)
- [T_CoInsurance_Info](#t_coinsurance_info) — 共保分单配置表
- [T_GzZrx_WorkType](#t_gzzrx_worktype) — 雇主责任险-雇员职业类型表
- [T_PProduct_PRCEnInsurance](#t_pproduct_prceninsurance)
- [T_Relation_InvoiceSpecSignInfo](#t_relation_invoicespecsigninfo) — 专票确认关系表
- [T_PProduct_AgreementRelation](#t_pproduct_agreementrelation) — 多险种合同与服务模板关系表
- [T_ZX_GoodsRecord](#t_zx_goodsrecord) — 振鑫小程序-商品兑换记录表
- [T_Guarantee_Claim](#t_guarantee_claim) — 保函索赔表
- [T_PProduct_QuitGuaranteeAuditLog](#t_pproduct_quitguaranteeauditlog)
- [T_CoInsurance_Log](#t_coinsurance_log) — 共保推送日志
- [T_XK_AuthRecord](#t_xk_authrecord) — 返点申请审核记录
- [T_PProduct_Annex](#t_pproduct_annex) — 多险种配置后台附件明细表
- [T_GzZrx_PackageOption](#t_gzzrx_packageoption) — 套餐方案表
- [T_GzZrx_HYX_Guarantee](#t_gzzrx_hyx_guarantee) — 货运险订单表
- [T_PProduct_Regulator](#t_pproduct_regulator)
- [T_PProduct_Claim](#t_pproduct_claim)
- [T_GzZrx_RoleMenus](#t_gzzrx_rolemenus) — 雇主责任险-角色菜单关系表
- [T_Coupon_Info](#t_coupon_info) — 优惠券发放使用记录表
- [T_Relation_PRCEnInsuranceAttach](#t_relation_prceninsuranceattach)
- [T_DaPingMu_LogOpenId](#t_dapingmu_logopenid) — 大屏幕日志推送openId
- [T_PProduct_BaseFile](#t_pproduct_basefile) — 附件基本类型表
- [T_PProduct_Serve](#t_pproduct_serve) — 多险种服务
- [T_GzZrx_RolesType](#t_gzzrx_rolestype) — 雇主责任险-用户角色类型表
- [T_Pay_Log_Intranet](#t_pay_log_intranet) — 支付记录表
- [T_Coupon_TaskLog](#t_coupon_tasklog) — 优惠券抽奖记录
- [T_Relation_PRCEnInsuranceEngagedesc](#t_relation_prceninsuranceengagedesc)
- [T_GzZrx_PRCInsurancePackage](#t_gzzrx_prcinsurancepackage) — 承保表与承保套餐关联表
- [T_PProduct_ServeCompany](#t_pproduct_servecompany) — 服务机构表
- [T_Enterprise_Black_ImportLog](#t_enterprise_black_importlog) — 黑名单拦截导入表
- [T_Pay_Log_CashierConfig](#t_pay_log_cashierconfig)
- [T_Relation_PRCEnInsuranceFileTemplate](#t_relation_prceninsurancefiletemplate)
- [T_PProduct_ClaimFile](#t_pproduct_claimfile)
- [T_PProduct_ServeDetail](#t_pproduct_servedetail)
- [T_Coupon_User](#t_coupon_user) — 优惠券用户统计表
- [T_Relation_PRCEnInsuranceTmpContent](#t_relation_prceninsurancetmpcontent) — 电子保函动态模板
- [T_PProduct_ClaimInfo](#t_pproduct_claiminfo)
- [T_PRC_Interface](#t_prc_interface)
- [T_PProduct_ServeDetailAttachment](#t_pproduct_servedetailattachment) — 服务细项附件列表
- [T_Enterprise_BlackPRC](#t_enterprise_blackprc) — 黑名单拦截设置表
- [T_CX_Order](#t_cx_order) — 订单表
- [T_GzZrx_Programme](#t_gzzrx_programme) — 方案表
- [T_PProduct_ClientMode](#t_pproduct_clientmode)
- [T_PRC_Info](#t_prc_info)
- [T_ZX_GuaranteeLog](#t_zx_guaranteelog) — 担保保函订单操作日志表
- [T_PProduct_ServeDetailInfo](#t_pproduct_servedetailinfo)
- [T_CX_Order_Group](#t_cx_order_group) — 团单配置表
- [T_SendMessage_Template](#t_sendmessage_template)
- [T_PProduct_ServeExpert](#t_pproduct_serveexpert) — 服务专家信息
- [T_PProduct_PRCEnInsuranceEnclosureGuarantee](#t_pproduct_prceninsuranceenclosureguarantee) — 附件存储表
- [T_ZX_ChannelRate](#t_zx_channelrate)
- [T_CX_PartnerChannel](#t_cx_partnerchannel) — 合作厂商-渠道
- [T_XK_Contacts_UpdateLog](#t_xk_contacts_updatelog) — 联系人更新记录表
- [T_SendMode_Info](#t_sendmode_info)
- [T_PProduct_ConstructionType](#t_pproduct_constructiontype)
- [T_PProduct_ServeExpertRalation](#t_pproduct_serveexpertralation) — 服务与专家关系表
- [T_GzZrx_Package](#t_gzzrx_package) — 保额套餐表
- [T_CX_Product](#t_cx_product) — 车险-产品表
- [T_Settle_Info](#t_settle_info) — 中心理赔资料表
- [T_GzZrx_PRCProgramme](#t_gzzrx_prcprogramme) — 二级渠道与方案关联表
- [T_PProduct_Department](#t_pproduct_department) — 机构部门网点
- [T_PProduct_ServeItem](#t_pproduct_serveitem) — 服务子项明细
- [T_XK_Contacts_DataStatistics](#t_xk_contacts_datastatistics) — 线客联系人出单数据监测统计表
- [T_StateMent_Files](#t_statement_files)
- [T_PProduct_DiversifiedFile](#t_pproduct_diversifiedfile)
- [T_PProduct_ServeItemInfo](#t_pproduct_serveiteminfo) — 服务明细信息（三和系统传入）
- [T_DaPingMu_User](#t_dapingmu_user)
- [T_StateMent_List](#t_statement_list)
- [T_PaymentSystem_Order](#t_paymentsystem_order)
- [T_PProduct_DiversifiedFileTemplate](#t_pproduct_diversifiedfiletemplate)
- [T_Email_Log](#t_email_log)
- [T_ZX_InsuranceShowItem](#t_zx_insuranceshowitem) — （已废弃）保函格式指定显示字段
- [T_GzZrx_PRCInsuranceProgramme](#t_gzzrx_prcinsuranceprogramme) — 承保表与方案表关联表
- [T_PProduct_ServeProject](#t_pproduct_serveproject) — 服务项目关联表
- [T_MobileMsg_DictType](#t_mobilemsg_dicttype)
- [T_Email_sendCode](#t_email_sendcode)
- [T_PRC_TypeModeSearchInfo](#t_prc_typemodesearchinfo)
- [T_StateMent_Log](#t_statement_log)
- [T_XK_OrderContacts](#t_xk_ordercontacts) — 线客，联系人与订单关系表
- [T_PProduct_DiversifiedFileTemplateBase](#t_pproduct_diversifiedfiletemplatebase)
- [T_ZX_Address](#t_zx_address) — 振鑫担保小程序-用户地址信息表
- [T_StateMent_Log2](#t_statement_log2)
- [T_PProduct_ServeRisk](#t_pproduct_serverisk)
- [T_Sys_Log](#t_sys_log)
- [T_PProduct_EmailLog](#t_pproduct_emaillog) — 履约发票邮件发送列表
- [T_RbRuleName](#t_rbrulename)
- [T_PrcOperation_Log](#t_prcoperation_log)
- [T_PProduct_ServeRiskAttachment](#t_pproduct_serveriskattachment) — 风险附件表

---

## T_Enterprise_AuditLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  | 0 |  |
| `cAuditMessage` | nvarchar(50) |  |  |  |  |  |
| `cAuditUserName` | nvarchar(20) |  |  |  |  |  |
| `CreateTime` | datetime |  |  |  |  |  |

## T_BrokerCompany_Info

*经纪公司表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cBrokerName` | nvarchar(30) |  |  |  |  | 经纪公司简称 |
| `cBrokerFullName` | nvarchar(50) |  |  |  |  | 经纪公司名称 |
| `cLogo` | varchar(200) |  |  |  |  | 经纪LOGO |
| `tCreateTime` | datetime |  |  |  |  | 添加日期 |
| `fIsDeleted` | tinyint |  |  | 否 | 0 | 是否删除，默认0否，1是 |

## T_changjiang_interface

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `Prc_id` | int |  |  |  |  |  |
| `Insurance_id` | int |  |  |  |  |  |
| `UserId` | nvarchar(50) |  |  |  |  |  |
| `PublicKey` | nvarchar(300) |  |  |  |  |  |
| `PrivateKey` | nvarchar(1050) |  |  |  |  |  |

## T_PProduct_Enclosure

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cEnclosureName` | varchar(200) |  |  |  |  |  |
| `cEnclosureCode` | varchar(50) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cLastEditUser` | nvarchar(50) |  |  |  |  | 最后修改人 |
| `tLastEditTime` | datetime |  |  |  |  | 最后修改时间 |
| `fFlieType` | tinyint |  |  |  |  | 文件类型 1图片 2文件 3压缩包 |

## T_PProduct_GuaranteeExtend

*履约订单表扩展*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cNewGuid` | varchar(50) | 是 |  | 否 |  | 关联履约报单表唯一标识 |
| `tEsignTime` | datetime |  |  |  |  | 签章时间 |
| `tPushTimeToUW` | datetime |  |  |  |  | 提交核保时间 |
| `fIsUnderWriting` | tinyint |  |  |  | 0 | 核保状态，默认0无，4待核保，6核保通过，9核保驳回 |
| `tUnderWritingTime` | datetime |  |  |  |  | 核保（审核、驳回）时间 |
| `cUnderWritingOpinion` | nvarchar(300) |  |  |  |  | 核保意见 |
| `cPaymentMethod` | nvarchar(30) |  |  |  |  | 支付方式（作废） |
| `tPayTime` | datetime |  |  |  |  | 支付时间 |
| `cPaymentType` | nvarchar(30) |  |  |  |  | 支付类型 |
| `cSourceCode` | varchar(50) |  |  |  |  | 业务推荐码 |
| `cBankCardNo` | varchar(50) |  |  |  |  | 基本户 |
| `fInvoiceType` | tinyint |  |  | 否 | 0 | 发票先选发票类型值 承保平台配置发票先选才有意义： 0 普票 2 专票 |
| `tGuaranteedTime` | datetime |  |  |  |  | 出单时间 |
| `fIsGuaranteed` | tinyint |  |  |  | 0 | 出单状态，默认0无，4待出单，6已出单 |
| `cInsuranceTypeNo` | varchar(50) |  |  |  |  | 险种编码 |
| `cPRCCode` | nvarchar(50) |  |  |  |  | 承保机构编码 |
| `cOrganName` | nvarchar(50) |  |  |  |  | 承保机构简称 |
| `cPaymentSerialNumber` | varchar(10) |  |  |  |  | 打款序列号 |
| `fEsignState` | tinyint |  |  | 否 | 0 | 签章状态 0 默认 1 待签章 4 已签章，5无需签章 |
| `cToEsignUrl` | varchar(200) |  |  |  |  | 待签章文件 |
| `tStartTime` | datetime |  |  |  |  | 投保须知打开时间 |
| `tEndTime` | datetime |  |  |  |  | 投保须知查看完成时间 |
| `cCode` | nvarchar(50) |  |  |  |  | 险种方案编码 |
| `fComputeMode` | int |  |  |  | 2 | 保费计算模式 1区间费率 2固定费率 3人工 |
| `fDockingMode` | tinyint |  |  |  | 1 | 对接模式  1保司接口出单 2线下人工出单，3线下出单，代出保单 |
| `fInvoiceCategory` | tinyint |  |  | 否 | 0 | 发票类型（0：增值税普通发票（电子发票）；2：增值税专用发票（纸质发票，邮寄送达邮费到付）） |
| `cDirectorname` | nvarchar(50) |  |  |  |  | 监管单位名称 |
| `cContactUserName` | nvarchar(50) |  |  |  |  | 被保险人联系人 |
| `cContactUserTel` | nvarchar(50) |  |  |  |  | 被保险人联系方式 |
| `cOwnerSheng` | varchar(10) |  |  |  |  | 被保险人省 |
| `cOwnerShi` | varchar(10) |  |  |  |  | 被保险人市 |
| `cOwnerQu` | varchar(10) |  |  |  |  | 被保险人区 |
| `cOwnerNature` | varchar(10) |  |  |  |  | 被保险企业性质 |
| `cAccessKey` | nvarchar(200) |  |  |  |  | 联银担保第三方推送URL地址 |
| `cZipUrl` | varchar(100) |  |  |  |  | 投保附件打包文件 |
| `fIsRejectnotice` | tinyint |  |  |  | 0 | 中心缴存状态通知接口，默认0无，1人社驳回（可退保、可批改），3缴存取消或申请退保（人社驳回后企业取消该缴存方式）（可退保），6, 缴存成功 |
| `tRejectnoticeTime` | datetime |  |  |  |  | 中心缴存驳回通知时间（申请退保时间） |
| `fIsPolicyFiling` | tinyint |  |  | 否 | 0 | 归档状态，默认0无，6已归档， |
| `fPremiumMode` | tinyint |  |  |  |  | 保费计算类型 1直接计算保费（先签章后审核） 2后置展示保费（先审核后签章） |
| `cFirmUUID` | varchar(50) |  |  |  |  | 影像uuid |
| `fPolicyType` | tinyint |  |  |  | 0 | 保单类型 1保单附凭证 2仅保单 3保单凭证各一份 |
| `cPolicyPzUrl` | varchar(500) |  |  |  |  | 保单凭证 |
| `cPostalCode` | varchar(50) |  |  |  |  | 投保人邮政编码 |
| `cBeneficiary` | nvarchar(50) |  |  |  |  | 受益人 |
| `cConstructionType` | nvarchar(30) |  |  |  |  | 最高建筑施工资质类型 |
| `cConstructionGrade` | nvarchar(30) |  |  |  |  | 最高建筑施工资质等级 |
| `fBusinessAmountType` | tinyint |  |  |  |  | 营业规模   1：营业收入>=8亿元；  2：6000万=<营业收入<8亿；   3：营业收入<6000万 |
| `fCompanyAmountType` | tinyint |  |  |  |  | 资产规模  1： 资产规模>=8亿元；  2：5000万=<资产规模<8亿；   3：资产规模<5000万 |
| `fApplyType` | int |  |  | 否 | 0 | 申请类型 1新保 2续保 3补缴 |
| `fApplyClaimAmount` | decimal(18,2) |  |  | 否 | 0 |  |
| `fRegulatorId` | int |  |  | 否 | 0 | 监管单位id |
| `fApplyPush` | int |  |  | 否 | 0 | 履约保函申请结果通知（0：未通知；1：已通知；） |
| `tApplyPushTime` | datetime |  |  |  |  | 履约保函申请结果通知时间 |
| `fIsInvalid` | tinyint |  |  | 否 | 0 | 失效状态，默认0否，1是 |
| `cQuitReason` | nvarchar(1000) |  |  |  |  | 申请退保原因 |
| `cContractFileUrl` | nvarchar(1000) |  |  |  |  | 合同文件 |
| `fHetongDays` | int |  |  | 否 | 0 | 合同期限 |
| `cRenewalOrder` | nvarchar(100) |  |  |  |  | 历史保单号 |
| `cContractFileName` | nvarchar(100) |  |  |  |  |  |
| `cRenewalPolicy` | varchar(100) |  |  |  |  |  |
| `ErrorInfo` | varchar(100) |  |  |  |  | 记录人保山西农民工异常信息 |
| `fMessageState` | int |  |  | 否 | 0 | 核保以及投保单号短信通知  0：未处理   1:投保通知发送成功 2:投保通知发送失败   3:核保通知发送成功 4:核保通知发送失败 |
| `cLocalPolicyUrl` | varchar(200) |  |  |  |  | 本地保单查询地址 |
| `cLocalPolicyPzUrl` | varchar(200) |  |  |  |  | 本地凭证查询地址 |
| `fEstimateRate` | decimal(10,3) |  |  |  |  | 预估费率 |
| `fEstimatePremium` | decimal(18,2) |  |  |  |  | 预估保费 |
| `fMoneyFrom` | tinyint |  |  |  |  | 项目资金来源(1:财政资金；2:企业自筹（银行信贷/机构投资/发行债券/租赁融资）) |
| `fAssets` | decimal(18,2) |  |  |  |  | 上一年度总资产（元） |
| `fDebt` | decimal(18,2) |  |  |  |  | 上一年度总负债（元） |
| `fDebtRate` | decimal(18,2) |  |  |  |  |  |
| `fIsSignFileAudit` | tinyint |  |  | 否 | 0 | 默认值0不需要签章文件审核，1签章文件待审核，2签章文件审核通过，3签章文件审核驳回 |
| `cSignFileAuditNotes` | nvarchar(100) |  |  |  |  | 签章文件审核意见 |
| `tSignFileAuditTime` | datetime |  |  |  |  | 签章文件审核时间 |
| `fIsMinDate` | tinyint |  |  |  |  | 是否限制最小保期 0不限制 1限制 |
| `fProjectType` | tinyint |  |  |  |  | 项目类型 1新建 2在建 |
| `tRenewalOrderEndTime` | datetime |  |  |  |  | 历史保单终保日期 |
| `tZBDate` | datetime |  |  |  |  | 中标日期 |
| `cPerformNo` | varchar(100) |  |  |  |  | 执行单号 |
| `tGuaranteedTime_limit` | datetime |  |  |  |  | 监管建议保险止期 |
| `cOrderOwner` | varchar(50) |  |  |  |  | 保单归属人 |
| `fMarginAmountHandleType` | int |  |  |  |  | 办理类型（1，项目保证金 2，企业保证金） |
| `ccentralProjectProvinceCode` | varchar(50) |  |  |  |  | 中心端 省编码 |
| `ccentralProjectCityCode` | varchar(50) |  |  |  |  | 中心端 市编码 |
| `ccentralProjectProvince` | varchar(100) |  |  |  |  | 中心端 省 |
| `ccentralProjectCity` | varchar(100) |  |  |  |  | 中心端 市 |
| `ccentralProjectArea` | varchar(100) |  |  |  |  | 中心端 区 |
| `ccentralProjectAreaCode` | varchar(50) |  |  |  |  | 中心端 区编码 |
| `cInsProgrammeName` | nvarchar(50) |  |  |  |  | 保险方案名称 |
| `fcInsProgrammeId` | int |  |  |  |  | 保险方案id |
| `cAccidentDesc` | nvarchar(500) |  |  |  |  | 进3年事故描述 |
| `fDelayApplyId` | int |  |  | 否 | 0 | 延期申请表id |
| `fForcedIssue` | tinyint |  |  | 否 | 0 | 是否强制人工出单，默认0否，1是 |
| `cFileUrl` | nvarchar(300) |  |  |  |  | 内蒙多险种弹框填单页附件 |
| `cPolicyNoPz` | varchar(50) |  |  |  |  | 凭证号 |
| `fIsMorePolicy` | tinyint |  |  | 否 | 0 | 是否多单 0 否 1 是 |
| `tFirstBegin` | datetime |  |  |  |  | 首单保险起期 |
| `fUserType` | int |  |  |  |  | 海南腾龙 同项目编号多次投保 用户类型不同 |
| `cChangeReason` | nvarchar(1000) |  |  |  |  |  |
| `cQuitOrderNo` | varchar(100) |  |  |  |  |  |
| `cQuitUserName` | varchar(100) |  |  |  |  |  |
| `cQuitUserPhone` | varchar(100) |  |  |  |  |  |
| `cOwerSincerityLevel` | varchar(100) |  |  |  |  |  |
| `cConstructionSincerityLevel` | varchar(100) |  |  |  |  |  |
| `tGuaranteedIntentionTimeBegin` | datetime |  |  |  |  |  |
| `tGuaranteedIntentionTimeEnd` | datetime |  |  |  |  |  |
| `fIsTestOrder` | tinyint |  |  | 否 | 0 |  |
| `fBusiId` | int |  |  | 否 | 0 | T_PProduct_PRCEnInsuranceBusiManager 表id |
| `fCheckUnderWriting` | tinyint |  |  |  | 0 | 核保是否复核，0否，1待复核，2已复核 |
| `tCheckUnderWritingTime` | datetime |  |  |  |  | 复核时间 |
| `cCheckUnderWritingOpinion` | nvarchar(300) |  |  |  |  | 核保复核意见 |
| `cBusiTips` | nvarchar(50) |  |  |  |  | 业务需求描述话术(用户填写) |
| `fFillFrom` | tinyint |  |  | 否 | 0 | 多险种填单来源，默认0中心过来，1后台填单（山西） |
| `fDepositType` | tinyint |  |  | 否 | 0 | 缓存类型，默认0无，1按预设比例缴存，3减少保证金应缴金额，5增加保证金应缴金额 |
| `fWarnInsuranceID` | int |  |  | 否 | 0 | 关联T_PProductWarn_Insurance表ID，山西填单用到 |
| `fIsMian` | tinyint |  |  |  | 0 | 是否主账号（0：否；1：是）（山西工资监管项目用） |
| `fAccountType` | tinyint |  |  |  | 0 | 账户类型（1：农民工工资专户；2：保证金账户；3：银行保函；4：工程担保公司保函；5：工程保证保险）（山西工资监管项目用） |
| `cInsuranceFullName` | nvarchar(50) |  |  |  |  | 保险公司全称 |
| `fAccountStatus` | tinyint |  |  |  | 0 | 账户状态  1:待验证,2:已校验,3:校验失败,4:注销,5：挂失,6：冻结,9：其他 |
| `fAccountSpec` | tinyint |  |  |  | 0 | 银行是否对账户设置特殊标识（0：否；1：是） |
| `cBranchName` | nvarchar(30) |  |  |  |  | 支行名称 |
| `fDiDepositAmount` | decimal(18,2) |  |  |  | 0 | 差异化存缴金额 |
| `cQuotationNo` | nvarchar(50) |  |  |  |  | 询价单号 |
| `tInvalidTime` | datetime |  |  |  |  | 失效时间 |
| `fBidderLevel` | tinyint |  |  |  | 0 | 投保企业信用等级 |
| `fPProductProgrammeID` | int |  |  | 否 | 0 | T_PProduct_Programme表id |
| `cChannelName` | varchar(255) |  |  |  |  | 渠道名称 |
| `cChannelCode` | varchar(255) |  |  |  |  | 渠道编码 |
| `cCoAssurer` | nvarchar(100) |  |  |  |  | 共同被保人 |
| `OrderId` | nvarchar(50) |  |  |  |  |  |
| `cSource` | nvarchar(50) |  |  |  |  | 自贡  ：数据来源，传值“企业新增/交易系统同步” |
| `cContent` | nvarchar(2000) |  |  |  |  | 自贡：人社审核意见 |
| `fIsPaidNotice` | int |  |  |  | 0 | 支付结果通知（个别地区需要，默认0 ，0未推送 1已推送） |
| `cGuaranteePurpose` | nvarchar(50) |  |  |  |  | 保函用途 |
| `fpayOnDemand` | int |  |  |  | 0 | 见索即付  （0：否；1：是） 杭州政采-联银用到 |
| `cHGCode` | nvarchar(50) |  |  |  |  |  |
| `cContactUserIDNumber` | nvarchar(50) |  |  |  |  |  |

## T_XK_RebateInfo

*返点信息表（主表）*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cNo` | varchar(17) |  |  |  |  | 申请编号 |
| `tCreateDate` | datetime |  |  | 否 | getdate() | 发起时间 |
| `cCreateUser` | nvarchar(20) |  |  |  |  | 创建人 |
| `cCreateUserID` | nvarchar(50) |  |  |  |  | 创建人ID，关联user表ID |
| `fCount` | int |  |  |  |  | 关联保单数量 |
| `fAmount` | decimal(18,2) |  |  |  |  | 返点金额 |
| `cUrl` | nvarchar(500) |  |  |  |  | 附件地址 |
| `fStatus` | tinyint |  |  |  |  | 审批状态（0：暂存状态；1：待审批；2：审批通过；3：审批驳回；4：已撤销） |
| `fRebateStatus` | tinyint |  |  |  | 1 | 返点状态（0：初始状态“/"，1：返点中；2：已返点） |
| `tReturnTime` | datetime |  |  |  |  | 标记返点时间 |
| `tPayDate` | datetime |  |  |  |  | 实际支付时间 |
| `cDesc` | nvarchar(200) |  |  |  |  |  |
| `fIsStatistics` | tinyint |  |  | 否 | 0 | 是否已经批量统计（0：还未批量统计；1：已经批量统计） |

## T_PProduct_ServeRiskResAttachment

*风险附件表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cServerRiskID` | nvarchar(200) |  |  | 否 |  |  |
| `cServerDetailID` | nvarchar(200) |  |  |  |  |  |
| `cFileName` | nvarchar(200) |  |  |  |  | 附件名称 |
| `cFileUrl` | varchar(200) |  |  |  |  | 附件地址 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cServeNum` | varchar(50) |  |  |  |  | T_PProduct_Serve关联字段cServeNum |
| `cFileDesc` | nvarchar(500) |  |  |  |  | 整改附件描述 |

## T_Enterprise_AuthActionRecord

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `tCreateDate` | datetime |  |  | 否 | getdate() |  |
| `cUser` | nvarchar(50) |  |  | 否 |  |  |
| `cActionName` | nvarchar(50) |  |  | 否 |  |  |
| `cDesc` | nvarchar(500) |  |  |  |  |  |
| `fEnterpriseInfoId` | int |  |  | 否 |  |  |
| `SysType` | varchar(10) |  |  | 否 |  |  |

## T_XK_RebateBatch

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cNo` | varchar(30) |  |  |  |  | 统计表批次 |
| `cUrl` | nvarchar(300) |  |  |  |  | 附件下载地址 |
| `cUrlName` | nvarchar(50) |  |  |  |  | 附件名称 |
| `tCreateTime` | datetime |  |  |  | getdate() | 批次生成时间 |
| `cCreateUser` | nvarchar(20) |  |  |  |  | 创建人 |
| `cCreateUserID` | nvarchar(50) |  |  |  |  | 创建人ID，关联user表ID |
| `fCount` | int |  |  |  |  | 关联保单数量 |
| `fRebateCount` | int |  |  |  |  | 关联申请单数量 |
| `fAmount` | decimal(18,2) |  |  |  |  | 返点金额 |
| `fStatus` | tinyint |  |  |  | 1 | 返点状态（1：返点中；2：已返点） |
| `tReturnTime` | datetime |  |  |  |  | 标记返点时间 |
| `tPayDate` | datetime |  |  |  |  | 实际支付时间 |
| `fType` | tinyint |  |  |  |  | 关联类型（1：支付宝；2：银行卡；0：全部-1.4版本加入） |

## t_toubaoNo_invalid

*投标编码失效表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Prc_Code` | varchar(50) | 是 |  | 否 |  | 平台编号 |
| `cInsuranceCode` | varchar(50) | 是 |  | 否 |  | 投标编码 |

## T_NJDT_User

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `LoginName` | nvarchar(20) |  |  | 否 |  |  |
| `Password` | nvarchar(50) |  |  | 否 |  |  |
| `RealName` | nvarchar(20) |  |  | 否 |  |  |
| `TelePhone` | varchar(50) |  |  | 否 |  |  |
| `fSex` | tinyint |  |  |  |  | 1:男0：女 |
| `fStatus` | tinyint |  |  |  | 1 | 状态（1：正常；0：禁用） |
| `tLastModifyDate` | datetime |  |  |  |  | 最后修改时间 |
| `tCreateDate` | datetime |  |  |  | getdate() | 创建时间 |
| `cUser` | nvarchar(50) |  |  |  |  | 操作人 |
| `fRoleId` | int |  |  |  |  | 角色id |
| `fChannelId` | int |  |  |  |  | 渠道id |
| `tLoginTime` | datetime |  |  |  |  |  |

## T_GzZrx_DataPermissions

*雇主责任险-数据权限表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Id` | varchar(50) | 是 |  | 否 |  |  |
| `CreateDateTime` | datetime |  |  | 否 |  | 创建时间 |
| `Description` | nvarchar(50) |  |  | 否 |  | 备注说明 |
| `IsDeleted` | bit |  |  | 否 |  | 删除状态，true是，false否 |
| `Name` | nvarchar(20) |  |  | 否 |  | 名称 |
| `fTag` | tinyint |  |  |  | 0 | 默认0传化责任险 |

## T_PProduct_ServeTemplate

*多险种服务模板*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `cServeTempNum` | varchar(50) | 是 |  | 否 | (0) | 模板编号 |
| `cServeTempName` | nvarchar(50) |  |  |  |  | 模板名称 |
| `cServeTempRemarks` | nvarchar(1000) |  |  |  |  | 模板备注 |
| `tCreateTime` | datetime |  |  |  |  | 创建时间 |
| `cOpUserID` | varchar(50) |  |  |  |  | 添加人账号ID |
| `cOpUserName` | varchar(50) |  |  |  |  | 添加人账号名称 |
| `platformCode` | varchar(50) |  |  |  |  | 平台编号 |
| `cInsuranceCompany` | nvarchar(30) |  |  |  |  | 保险公司，比如人保 |
| `fState` | int |  |  |  | 0 | 状态 0停用 1启用 |
| `cServeTempFileUrl` | nvarchar(500) |  |  |  |  | 模板文件 |
| `cPRCEnInsuranceID` | nvarchar(MAX) |  |  |  |  | 承保平台ID |
| `cUserID` | nvarchar(200) |  |  |  |  | 用户ID |

## T_GzZrx_GuaranteeEmployee

*雇主责任险--参保雇员信息*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fMianID` | int |  |  | 否 |  |  |
| `fGuaranteeId` | int |  |  | 否 |  |  |
| `cName` | nvarchar(50) |  |  | 否 |  | 姓名 |
| `cCardID` | varchar(20) |  |  | 否 |  | 身份证号 |
| `fPackageOptionId` | int |  |  | 否 | 0 | 职业类别ID（废弃） |
| `tStartTime` | datetime |  |  | 否 |  | 生效时间 |
| `tEndTime` | datetime |  |  | 否 |  | 截止时间 |
| `fState` | tinyint |  |  |  |  | 状态（0：正常投保；1：批增；2：批减(替换)） |
| `fTBState` | tinyint |  |  |  | 0 | 投保状态（0：未投保；1：已投保；3：作废）保司回调更新状态 |
| `tCreateTime` | datetime |  |  |  | getdate() |  |
| `fIsDelete` | tinyint |  |  | 否 | 0 | 是否删除（0：未删除；1：已删除） |
| `cUser` | nvarchar(50) |  |  |  |  |  |
| `cModifyUser` | nvarchar(50) |  |  |  |  | 修改人 |
| `tLastModifyDate` | datetime |  |  |  |  | 最后修改时间 |
| `fSex` | tinyint |  |  | 否 | 0 | 性别（0：女；1：男） |
| `fAge` | int |  |  | 否 |  | 年龄 |
| `cWorkName` | nvarchar(50) |  |  | 否 |  | 职业别名 |
| `fPremium` | decimal(18,2) |  |  | 否 | 0 | 保费 |
| `fPGGuaranteeId` | int |  |  | 否 | 0 | 操作批减的批单id |
| `fReplacedId` | int |  |  | 否 | 0 | 替换当前记录的雇员记录id（新雇员对应的id） |
| `cPackageOptionCode` | nvarchar(50) |  |  |  |  | T_GzZrx_PackageOption 表 cOptionCode |
| `fOldId` | int |  |  | 否 | 0 | 追溯id。老的记录id |

## T_MobileMsg_Dict

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `cTypeCode` | varchar(20) |  |  | 否 |  | 字典类型编码，关联T_CDSP_DictType表的cTypeCode |
| `cName` | nvarchar(30) |  |  | 否 |  | 字典项名称 |
| `cCode` | varchar(50) | 是 |  | 否 |  | 字典项编码 |
| `cBz` | nvarchar(50) |  |  |  |  | 备注项 |
| `fSort` | int |  |  | 否 | 0 | 排序 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `fIsDelete` | bit |  |  |  | 0 | 是否删除，默认0否，1是 |

## T_Enterprise_AuthAttachment

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cPicUrl` | nvarchar(500) |  |  | 否 |  |  |
| `tCreateDate` | datetime |  |  | 否 |  |  |
| `fType` | tinyint |  |  | 否 |  |  |
| `fEnterpriseInfoId` | int |  |  | 否 |  |  |
| `SysType` | int |  |  | 否 |  |  |
| `tLastModifyDate` | datetime |  |  |  |  |  |

## T_tsign_Authentication

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  | 否 |  | 企业ID |
| `cEnterpriseName` | nvarchar(50) |  |  | 否 |  | 企业名称 |
| `cBank` | nvarchar(50) |  |  |  |  |  |
| `cBankCardNo` | varchar(50) |  |  | 否 |  | 基本户帐号 |
| `amount` | decimal(10,2) |  |  | 否 |  | 随机金额 |
| `fstate` | tinyint |  |  | 否 | 0 | 认证状态，0：未认证，1：已认证 |
| `fpayId` | int |  |  | 否 | 0 | 付款记录表ID |
| `cBankVoucher` | varchar(200) |  |  |  |  |  |
| `tUpTime` | datetime |  |  |  |  |  |
| `type` | tinyint |  |  | 否 | 0 |  |

## T_PProduct_EnterpriseAccount

*企业子账号信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  | 否 |  | 企业表id |
| `cName` | nvarchar(50) |  |  |  |  | 姓名 |
| `cMobile` | varchar(50) |  |  |  |  | 手机号 |
| `cPwd` | varchar(100) |  |  |  |  | 密码 |
| `cPosition` | nvarchar(50) |  |  |  |  | 岗位 |
| `cDesc` | nvarchar(300) |  |  |  |  | 备注 |
| `tCreateTime` | datetime |  |  |  |  | 创建日期 |
| `fState` | tinyint |  |  | 否 | 1 | 状态（0：停用；1：启用） |

## T_XK_Order

*线客订单表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fPlatformID` | int |  |  | 否 | 0 | 关联T_XK_Platform表ID |
| `fContactsID` | int |  |  |  | 0 | 关联T_XK_Contacts表ID |
| `fDataFrom` | tinyint |  |  |  | 0 | 数据来源，1业务系统，2手动创建 |
| `cPolicyNo` | varchar(50) |  |  |  |  | 保单号 |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 投保企业名称 |
| `cBidName` | nvarchar(200) |  |  |  |  | 标段名称 |
| `cInsuranceCompany` | nvarchar(20) |  |  |  |  | 金融机构 |
| `fPremium` | decimal(18,2) |  |  |  | 0 | 保费 |
| `fRate` | decimal(10,4) |  |  |  | 0 | 费率 |
| `fState` | tinyint |  |  |  |  | 订单状态，1已退保，6已出函 |
| `tGuaranteedTime` | datetime |  |  |  |  | 出函时间 |
| `fBidTime` | datetime |  |  |  |  | 开标时间 |
| `cBz` | nvarchar(500) |  |  |  |  | 备注 |
| `fRebateRatio` | decimal(10,4) |  |  |  | 0 | 返点比例 |
| `fRebateAmount` | decimal(18,2) |  |  |  |  | 返点金额 |
| `fRebateStatus` | tinyint |  |  |  | 0 | 返点状态（0：初始状态“/"，1：返点中；2：已返点；） |
| `tRebateTime` | datetime |  |  |  |  | 返点时间 |
| `fReturnStatus` | tinyint |  |  |  | 0 | 标记已退状态(0: 未标记，1: 已标记，2：已标记已退 |
| `cSourceCode` | nvarchar(50) |  |  |  |  | 邀请码 |
| `tCreateTime` | datetime |  |  |  |  | 创建时间 |
| `cCreateUser` | nvarchar(20) |  |  |  |  | 创建人 |
| `cCreateUserID` | nvarchar(50) |  |  |  |  | 创建人ID，关联user表ID |
| `fIsDeleted` | tinyint |  |  |  | 0 | 删除状态，默认0无，1已删除 |
| `fTotalRebateAmount` | decimal(18,2) |  |  |  | 0 | 累计已申请返点金额（包含待审批、审批通过） |
| `tReturnTime` | datetime |  |  |  |  | 申请时间（标记已退时间） |
| `tPayDate` | datetime |  |  |  |  | 实际支付时间 |
| `fIsManul` | tinyint |  |  | 否 | 0 | 是否手动标记退回（0：否；1：是） |

## T_OnlineInvoice_User

*线上开票-用户表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `cUserTel` | varchar(20) | 是 |  | 否 |  | 注册手机 |
| `fState` | tinyint |  |  |  | 0 | 账号状态 0待审核 1禁用 2正常 |
| `tLoginTime` | datetime |  |  |  |  | 上一次登录时间 |
| `tLoginIP` | varchar(20) |  |  |  |  | 上一次登录IP |
| `fLoginErrCount` | int |  |  |  |  | 登录错误次数，当日累计错误＞3次，24小时后才能再登 |
| `fQueryErrCount` | int |  |  |  |  | 空搜错误累计3次冻结账号，24小时后才能继续 |
| `CreateTime` | datetime |  |  | 否 | getdate() |  |

## T_PProduct_ServeTemplateServeDetail

*模板服务项明细*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fTemplateID` | int |  |  | 否 |  |  |
| `fItemID` | nvarchar(200) |  |  |  |  |  |
| `fDetailID` | nvarchar(200) |  |  |  |  |  |
| `cItemName` | nvarchar(200) |  |  |  |  |  |
| `cItemDetailName` | nvarchar(200) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |

## T_XK_Platform

*线客平台表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fBusinessType` | tinyint |  |  | 否 | 0 | 业务类型 0 纯线客业务 1 投标业务 2 纯经纪业务 3 代收业务 |
| `cInsuranceType` | varchar(20) |  |  | 否 | '' | 险种 取字典数据 |
| `cRelPlatformCode` | varchar(30) |  |  |  |  | 关联平台编码 |
| `cPlatformCode` | varchar(30) |  |  | 否 |  | 平台编号 |
| `cPlatformName` | nvarchar(50) |  |  | 否 |  | 平台名称 |
| `cCity` | nvarchar(30) |  |  |  |  | 省/市/区 |
| `cSheng` | nvarchar(30) |  |  |  |  | 省 |
| `cShi` | nvarchar(30) |  |  |  |  | 市 |
| `cQu` | nvarchar(30) |  |  |  |  | 区 |
| `cInsuranceName` | nvarchar(10) |  |  |  |  | 金融机构 |
| `cInstName` | nvarchar(50) |  |  |  |  | 承保机构 |
| `cTdpName` | nvarchar(30) |  |  |  |  | 技术商 |
| `cOrgName` | nvarchar(50) |  |  |  |  | 经纪公司 |
| `cFileUrl` | varchar(200) |  |  |  |  | 协议附件 |
| `cRemark` | nvarchar(200) |  |  |  |  | 备注 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |
| `fTagType` | tinyint |  |  | 否 | 0 | 线客业务标记方式 0 返点业务订单 1 人工标记(渠道码)订单 2 平台订单自动标记 |
| `fState` | tinyint |  |  | 否 | 1 | 状态 1 启用 0 禁用 |

## T_tsign_Evidence

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `fGuaranteeID` | int |  |  |  |  |  |
| `C_Evid` | nvarchar(50) |  |  |  |  | 证据链编号 |
| `Standard_Evid` | nvarchar(50) |  |  |  |  | 证据点ID |
| `EvidenceUrl` | nvarchar(500) |  |  |  |  | 存证凭证url |
| `createTime` | datetime |  |  |  | getdate() |  |

## T_NJDT_Role

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cRoleName` | nvarchar(50) |  |  |  |  | 角色名称 |
| `cRoleCode` | nvarchar(50) |  |  |  |  | 角色标识 |
| `fSort` | int |  |  |  |  |  |
| `fStatus` | tinyint |  |  | 否 | 1 | 状态（0：禁用；1：启用） |
| `tCreateDate` | datetime |  |  |  | getdate() |  |

## T_ZX_UserEnterprise

*振鑫小程序-用户企业关联表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fZXUserID` | int |  |  |  |  | 关联T_ZX_User表ID |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `fType` | tinyint |  |  |  | 0 | 企业类型，0绑定，1添加 |
| `fIsDeleted` | tinyint |  |  | 否 | 0 |  |
| `cInvitationCode` | nvarchar(50) |  |  |  |  | 绑定邀请码 |

## T_GzZrx_Channel

*雇主责任险一级渠道表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cChannelCode` | varchar(50) |  |  | 否 |  | 一级渠道编码 |
| `cChannelName` | nvarchar(50) |  |  | 否 |  | 一级渠道名称 |
| `cChannelShortName` | nvarchar(20) |  |  | 否 |  | 一级渠道简称 |
| `fState` | tinyint |  |  | 否 | 0 | 状态 0 禁用 1 启用 |
| `cRemark` | nvarchar(100) |  |  |  |  | 平台介绍 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |

## T_PProductYz_Cliam

*医责险-理赔*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fGuaranteeId` | int |  |  | 否 |  | 保单表id   T_PProductYz_Guarantee |
| `fMedicalAccidentId` | int |  |  | 否 |  | 事故表id   T_PProductYz_MedicalAccident |
| `cCaseNo` | varchar(50) |  |  | 否 |  | 保险公司报案号 |
| `fApplyAmount` | decimal(18,2) |  |  | 否 |  | 申请赔付金额 |
| `cApplyAttachUrl` | nvarchar(200) |  |  | 否 |  | 赔付申请附件 |
| `fStatus` | tinyint |  |  |  | 1 | 状态（1：已受理，2：已撤销；3：赔付成功；4：拒绝赔付） |
| `fPayAmount` | decimal(18,2) |  |  |  | 0 | 实际赔付金额 |
| `tCancelTime` | datetime |  |  |  |  | 撤销理赔时间 |
| `cCancelUser` | nvarchar(50) |  |  |  |  | 撤销理赔操作人 |
| `cCancelReason` | nvarchar(200) |  |  |  |  | 撤销原因 |
| `tCloseTime` | datetime |  |  |  |  | 结案时间 |
| `cCloseUser` | nvarchar(50) |  |  |  |  | 结案操作人 |
| `cCloseAttachUrl` | varchar(300) |  |  |  |  | 结案附件 |
| `tCreateDate` | datetime |  |  |  | getdate() |  |
| `cUserName` | nvarchar(50) |  |  |  |  | 理赔申请创建人 |
| `fShowYTW` | tinyint |  |  | 否 | 1 | 是否展现给医调委（0：不展现；1：展现） |
| `fShowCG` | tinyint |  |  | 否 | 1 | 是否展现给从共（0：不展现；1：展现） |
| `fTPStatus` | tinyint |  |  | 否 | 0 | 摊赔状态（0：未开始；1：进行中；2：已完成）。理赔完成后，状态0改成1，所有摊赔记录都确认后，1改成2 |
| `fTPFinishTime` | datetime |  |  |  |  | 全部摊赔完成时间 |
| `fIsSendMsg` | tinyint |  |  | 否 | 0 | 是否发送摊赔超时短信（0：未发送；1：已发送） |
| `tTPStartTime` | datetime |  |  |  |  | 发起摊赔时间 |

## T_PProduct_EnterpriseAttachment

*农民工履约企业附件表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `cName` | nvarchar(100) |  |  |  |  | 附件文件名称 |
| `cUrl` | varchar(200) |  |  |  |  |  |
| `CreateTime` | datetime |  |  |  |  |  |
| `fIsDelete` | bit |  |  |  | 0 | 是否删除（0否，1是 |
| `fPid` | int |  |  |  | 0 |  |
| `fSid` | int |  |  |  | 0 |  |

## T_tsign_Guarantee

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `pdfOssUrl` | nvarchar(300) |  |  |  |  | 对应T_Guarantee_Info cEsignUrl 字段做唯一关联 |
| `signServiceId` | nvarchar(50) |  |  |  |  |  |
| `certificateInfoUrl` | nvarchar(500) |  |  |  |  | 查看链接 |
| `createTime` | datetime |  |  |  | getdate() |  |
| `systype` | nvarchar(10) |  |  |  |  | 系统类型 存证证据链、退保证明 |
| `platformCode` | nvarchar(50) |  |  |  |  | 平台编号 |
| `IssuingAgencyNo` | nvarchar(50) |  |  |  |  | 出单机构编号 |
| `fType` | tinyint |  |  |  | 0 | 0:e签宝2.0； 1：e签宝3.0；2：e签宝-天印 |
| `fGuaranteeType` | tinyint |  |  |  | 0 | 1. 多险种；2：投标 |
| `fGuaranteeId` | int |  |  |  |  |  |
| `cNo` | nvarchar(50) |  |  |  |  | 签章序列号，多次签章传相同信息 |
| `sealId` | nvarchar(50) |  |  |  |  | 章模id |
| `fileKey` | nvarchar(50) |  |  |  |  |  |

## T_PProduct_SettleInfo

*履约理赔申请资料表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  | 0 | 关联企业表ID |
| `fGuaranteeInfoID` | int |  |  |  | 0 | 关联订单表ID |
| `cBz` | nvarchar(MAX) |  |  |  |  | 备注 |
| `cUrl` | varchar(250) |  |  |  |  | 资料上传地址 |
| `CreateTime` | datetime |  |  |  | getdate() |  |
| `fIsPush` | bit |  |  |  | 0 | 是否已推送，默认0否，1是 |
| `tPushTime` | datetime |  |  |  |  | 推送时间 |
| `fState` | tinyint |  |  |  | 0 | 状态 |

## T_Esign_UserDataAccess

*签章管理员设置*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cUserId` | nvarchar(50) | 是 |  | 否 |  |  |
| `fIsAdmin` | tinyint |  |  | 否 | 1 | 是否签章管理员权限（0：否；1：是） |

## T_Enterprise_RemarkLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  | 否 | 0 |  |
| `cRemark` | nvarchar(300) |  |  |  |  |  |
| `cUserName` | nvarchar(20) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  |  |  |
| `platformcode` | varchar(50) |  |  |  |  |  |
| `Prc_Type` | tinyint |  |  |  | 0 |  |

## T_PProduct_ExecutePolicyInfo

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cPerformNo` | nvarchar(200) |  |  |  |  | 执行单号 |
| `tApplyTime` | datetime |  |  |  |  | 申请时间 |
| `fPayable` | decimal(18,2) |  |  |  |  | 保证金保额。单位元。 |
| `fCapital` | decimal(18,2) |  |  |  |  | 使用/解除监管金额（0-4位小数）单位元（使用和解除监管时有） |
| `cAcctName` | nvarchar(200) |  |  |  |  | 工资专户账户名称（使用时有） |
| `cAcctNo` | nvarchar(200) |  |  |  |  | 工资专户账号（使用时有） |
| `cBankName` | nvarchar(200) |  |  |  |  |  |
| `cUnitedCode` | nvarchar(200) |  |  |  |  | 工资专户开户行的内蒙总行联行号（使用时有） |
| `cCheckOrg` | nvarchar(200) |  |  |  |  | 审核主管单位 |
| `tCheckTime` | datetime |  |  |  |  | 审核通过时间 |
| `cSignNo` | nvarchar(200) |  |  |  |  | 签约编号 |
| `cDepositType` | nvarchar(200) |  |  |  |  |  |
| `cExecType` | nvarchar(200) |  |  |  |  | 保单类型3：保单 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `fProjectID` | int |  |  |  |  | 项目ID |
| `tStartDate` | datetime |  |  |  |  | 起始有效期(格式yyyy-mm-dd) |
| `tEndDate` | datetime |  |  |  |  | 计划延长工期(格式yyyy-mm-dd) |
| `fGuaranteeID` | int |  |  |  |  |  |
| `fCreateState` | int |  |  |  |  |  |
| `fEnterpriseID` | int |  |  |  |  |  |
| `cComName` | nvarchar(200) |  |  |  |  |  |
| `cComCode` | nvarchar(200) |  |  |  |  |  |
| `fType` | tinyint |  |  | 否 | 0 |  |

## T_MobileMsg_ChannelSign

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cChannel` | varchar(50) |  |  |  |  | 渠道，关联T_MobileMsg_Dict表字段cCode |
| `cSignature` | varchar(50) |  |  |  |  | 签名，关联T_MobileMsg_Dict表字段cCode |
| `fState` | tinyint |  |  |  | 0 | 状态：0申请中，1有效中，2已失效，3巡检异常 |
| `cCreateUser` | nvarchar(50) |  |  |  |  | 创建人 |
| `cCreateUserID` | varchar(50) |  |  |  |  | 创建人ID |
| `tCreateTime` | datetime |  |  |  |  | 创建时间 |
| `tSendTime` | datetime |  |  |  |  | 最近巡检时间 |
| `cBz` | nvarchar(200) |  |  |  |  | 备注 |

## T_PayLog_Manual

*模拟支付记录信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fType` | tinyint |  |  | 否 | 1 | 类型（1：投标业务；2：代收代付） |
| `cNewGuid` | nvarchar(50) |  |  | 否 |  |  |
| `fPayId` | int |  |  | 否 |  |  |
| `cDDNo` | nvarchar(50) |  |  |  |  |  |
| `tCreateDate` | datetime |  |  | 否 | getdate() |  |
| `cUser` | nvarchar(50) |  |  | 否 |  | 操作人 |

## T_tsign_NSH

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `thirdPartyUserId` | nvarchar(50) | 是 |  | 否 |  |  |
| `name` | nvarchar(50) |  |  |  |  |  |
| `idNumberGR` | nvarchar(50) |  |  |  |  | 身份证号码 |
| `idNumberJG` | nvarchar(50) |  |  |  |  | 统一社会信用代码 |
| `mobile` | nvarchar(20) |  |  |  |  | 手机号码 |
| `email` | nvarchar(50) |  |  |  |  | 邮箱地址 |
| `accountIdGR` | nvarchar(50) |  |  |  |  | 个人账号 |
| `accountIdJG` | nvarchar(50) |  |  |  |  | 机构账号 |
| `orgId` | nvarchar(50) |  |  |  |  |  |
| `createTime` | datetime |  |  |  | getdate() |  |
| `updateTime` | datetime |  |  |  |  |  |
| `AppId` | nvarchar(50) |  |  |  |  | 项目ID 正式上线时需要分配 |
| `App_Secret` | nvarchar(50) |  |  |  |  | 项目Secret 正式上线时需要分配 |
| `prcCode` | nvarchar(50) |  |  |  |  | 内部项目标识 |
| `sealId` | nvarchar(50) |  |  |  |  | 印章ID，通过e签宝官网获取对应实名主体下的印章编号。 如果为配置则用这个账号下默认章 |

## T_PProduct_SuperviseMode

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cModeName` | nvarchar(50) |  |  |  |  | 模式名称 |
| `cModeCode` | nvarchar(50) |  |  |  |  | 模式编码 |
| `cModeDescribe` | nvarchar(500) |  |  |  |  | 模式描述 |
| `fAuditType` | tinyint |  |  |  |  | 保证金审核类型 |
| `fArtificialAuditType` | tinyint |  |  |  |  | 人社人工审核保证金内容 |
| `fPolicyType` | tinyint |  |  |  |  | 凭证审核类型 |
| `fAutoCalculation` | tinyint |  |  |  |  | 是否需要自动计算农民工保证金预估金额 |
| `fIsOnline` | tinyint |  |  |  |  | 是否支持线上办理 |
| `fIsOffline` | tinyint |  |  |  |  | 是否支持线下办理 |
| `fNecessaryRate` | tinyint |  |  |  |  | 线下出单费率是否必填 |
| `fNecessaryPremium` | tinyint |  |  |  |  | 线下出单费用（保费）是否必填 |
| `fOfflineInsuranceType` | tinyint |  |  |  |  | 线下出单机构控制 |
| `fOfflinePolicyType` | tinyint |  |  |  |  | 线下出单凭证类型 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `fClaimaAuditType` | tinyint |  |  |  |  | 理赔审核类型 ① 理赔发起人直接核定
② 理赔发起人审核，如有上级部门，上级部门复核，无上级部门则直接核定
③ 免核，系统自动测算 |
| `fDelayAuditType` | tinyint |  |  |  |  | 延期审核类型：
① 区县级部门核定
② 市级部门核定
③ 区县部门核定特殊情况市级部门复核
④ 免核，系统自动测算 |
| `fFinishedAuditType` | tinyint |  |  |  |  | 完工审核类型：
① 区县级部门核定
② 市级部门核定
③ 区县部门核定特殊情况市级部门复核
④ 免核，系统自动测算 |
| `cOnlinePayType` | nvarchar(200) |  |  |  |  | 线上办理支持的缴纳类型 |
| `cOfflinePayType` | nvarchar(200) |  |  |  |  | 线下办理支持的缴纳类型 |
| `fOfflineVUploadType` | tinyint |  |  |  |  | 线下出单凭证上传主体，0施工单位上传，1监管部门上传 |

## T_EnterpriseDiscount_CardID

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fPRCEnInsuranceId` | int |  |  | 否 |  |  |
| `cPrefix` | varchar(50) |  |  |  |  |  |
| `fIndex` | int |  |  |  |  |  |
| `cCardID` | varchar(50) |  |  |  |  |  |

## T_PProduct_Files

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `platformCode` | varchar(50) |  |  |  |  | 平台编码 |
| `cRequestId` | varchar(50) |  |  |  |  | 请求标识，对应T_PProduct_Guarantee表cRequestId |
| `typeName` | nvarchar(50) |  |  |  |  | 文件类型名 |
| `fwptCode` | varchar(50) |  |  |  |  | 类型标识 |
| `cNewGuid` | varchar(50) |  |  |  |  | 唯一标识 |
| `CreateTime` | datetime |  |  |  |  |  |

## T_tsign_PayLog

*支付记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `transno` | varchar(50) | 是 |  | 否 |  | 银行流水号 |
| `transtime` | datetime |  |  | 否 |  | 支付时间 |
| `transamount` | decimal(18,2) |  |  | 否 |  | 支付金额 |
| `payeracctno` | varchar(50) |  |  | 否 |  | 付款卡号 |
| `payeracctname` | nvarchar(50) |  |  | 否 |  | 付款户名 |
| `abstractinfo` | nvarchar(50) |  |  |  |  | 备注 |
| `oppositebankno` | varchar(50) |  |  | 否 |  | 付款行号 |
| `oppositebankname` | nvarchar(50) |  |  | 否 |  | 付款行名 |
| `tdate` | datetime |  |  | 否 | getdate() | 日期 |
| `OrderNo` | varchar(50) |  |  |  |  | 订单号 |
| `fState` | tinyint |  |  | 否 | 0 | 0:未使用，1：已使用，2：退款中，3：已退款 |

## T_PProduct_SupervisePRC

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cPRCCode` | nvarchar(50) |  |  |  |  | 监管渠道编码 |
| `cPRCFullName` | nvarchar(50) |  |  |  |  | 监管渠道全称 |
| `cPRCName` | nvarchar(50) |  |  |  |  | 监管渠道简称 |
| `cCityFullName` | nvarchar(50) |  |  |  |  | 业务渠道所在地 |
| `cPlatformProvince` | nvarchar(50) |  |  |  |  | 业务渠道所在省编码 |
| `cPlatformCity` | nvarchar(50) |  |  |  |  | 业务渠道所在市编码 |
| `cPlatformCounty` | nvarchar(50) |  |  |  |  | 业务渠道所在县编码 |
| `cWebTitle` | nvarchar(100) |  |  |  |  | 监管端登录页面-网站一级标题 |
| `cWebLoginTitle` | nvarchar(100) |  |  |  |  | 监管端登录页面-登录框标题 |
| `cWebLoginLogo` | nvarchar(200) |  |  |  |  | 页面标签logo |
| `cWebDomain` | nvarchar(200) |  |  |  |  | 监管端网站地址 |
| `cPreFormalUrl` | nvarchar(200) |  |  |  |  | 监管端网站地址不带http |
| `cEnterpriseWebTitle` | nvarchar(200) |  |  |  |  | 企业端登录页面-网站一级标题 |
| `cEnterpriseWebLoginTitle` | nvarchar(200) |  |  |  |  | 企业端登录页面-登录框标题 |
| `cEnterpriseWebLoginLogo` | nvarchar(200) |  |  |  |  | 企业端页面标签logo |
| `cEnterpriseWebDomain` | nvarchar(200) |  |  |  |  | 企业端网站域名 |
| `cEnterprisePreFormalUrl` | nvarchar(200) |  |  |  |  | 企业端网站域名（不带http） |
| `fAuthType` | int |  |  |  | 0 | 企业端认证类型 1免认证 2我司打款认证 |
| `cCoordinate` | varchar(50) |  |  |  |  | 经纬度配置 |
| `cCustomerServiceUserID` | varchar(50) |  |  |  |  | 客服ID |
| `cCustomerServiceLinkUrl` | nvarchar(200) |  |  |  |  | 客服链接 |
| `cWebFoot` | nvarchar(500) |  |  |  |  | 网站底栏配置 |
| `fState` | tinyint |  |  |  |  | 状态 0停用 1启用 |
| `cCustomerServiceCode` | varchar(50) |  |  |  |  | 客服QQ号 |
| `cCustomerServicePhone` | varchar(50) |  |  |  |  | 客服电话 |
| `fOrderWaringDay` | int |  |  |  |  | 保单到期预警天数 |
| `fHandleWaringDay` | int |  |  |  |  | 新缴未备案预警天数 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cPlatformProvinceCode` | nvarchar(50) |  |  |  |  | 业务渠道所在省编码 |
| `cPlatformCityCode` | nvarchar(50) |  |  |  |  | 业务渠道所在市编码 |
| `cPlatformCountyCode` | nvarchar(50) |  |  |  |  | 业务渠道所在县编码 |
| `fRenewalWaringDay` | int |  |  |  |  | 续缴未备案预警天数 |
| `fMakeUpWaringDay` | int |  |  |  |  | 补缴未备案预警天数 |
| `fFinishedWaringDay` | int |  |  |  |  | 完工/延期未确认预警天数 |

## T_EnterpriseDiscount_ImportLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cFileName` | nvarchar(50) |  |  |  |  |  |
| `cFileUrl` | nvarchar(200) |  |  | 否 |  |  |
| `tCreateDate` | datetime |  |  |  | getdate() |  |
| `fPRCEnInsuranceId` | int |  |  | 否 |  |  |
| `fType` | tinyint |  |  | 否 | 1 |  |

## T_tsign_Seal

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `organizeAccountId` | varchar(50) | 是 |  | 否 |  | e签宝用户ID |
| `OssUrl` | varchar(100) |  |  |  |  | 签章文件保存路径(标准公章) |
| `enterpriseName` | nvarchar(100) |  |  |  |  |  |
| `createTime` | datetime |  |  |  | getdate() | 创建时间 |
| `updateTime` | datetime |  |  |  |  |  |
| `socialCreditCode` | nvarchar(36) |  |  |  |  | 社会信用代码 |
| `pdfOssUrl` | nvarchar(300) |  |  |  |  | 签署成功后的pdf阿里云oss地址 |
| `enterprisePhone` | varchar(50) |  |  |  |  | 企业手机号码 |
| `signServiceId` | varchar(50) |  |  |  |  |  |
| `accountType` | tinyint |  |  |  |  | 1 = 个人账号 |
| `ErrorInfor` | nvarchar(50) |  |  |  |  |  |
| `contractOssUrl` | varchar(100) |  |  |  |  | 合同专用章-印章类型 |
| `financeOssUrl` | varchar(100) |  |  |  |  | 财务专用章-印章类型 |
| `officialOssUrl` | varchar(100) |  |  |  |  | 公章(内部系统)-印章类型 |
| `isDifferentSeals` | tinyint |  |  | 否 | 0 | 是否允许用不同的印章进行盖章 1是 0否 |

## T_NJDT_RoleMenu

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |
| `IsDeleted` | bit |  |  | 否 | 0 |  |
| `MenuId` | int |  |  |  |  |  |
| `RoleId` | int |  |  |  |  |  |

## T_PProduct_FilesUrl

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  |  |  | 对应T_PProduct_Files表cNewGuid |
| `suffix` | varchar(30) |  |  |  |  | 文件后缀名 |
| `url` | varchar(300) |  |  |  |  | 文件下载URL |
| `CreateTime` | datetime |  |  |  |  |  |

## T_MobileMsg_BatchLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cBatchNo` | varchar(30) |  |  | 否 |  | 批次序号 |
| `fChannelSignID` | int |  |  | 否 | 0 | T_MobileMsg_ChannelSign表id |
| `fLogID` | int |  |  | 否 |  | T_MobileMsg_Log表id |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_tsign_SceneDataDictionary

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `BusinessTempletId` | nvarchar(50) |  |  |  |  | 所属行业类型ID |
| `SceneTempletId` | nvarchar(50) |  |  |  |  | 业务凭证（名称）ID |
| `SegmentTempletId` | nvarchar(50) |  |  |  |  | 证据点名称ID |

## T_OnlineInvoice_InvoiceInfo

*发票信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 企业名 |
| `cEnterpriseNameCode` | varchar(50) |  |  |  |  | 企业信用代码 |
| `fOnlineUserID` | int |  |  |  |  | 用户账号Id |
| `fType` | tinyint |  |  |  | 0 | 0普票电子发票，1普票纸质发票，2专票纸质发票 |
| `cUser` | nvarchar(20) |  |  |  |  | 联系人 |
| `cUserPhone` | varchar(50) |  |  |  |  | 税务登记电话 |
| `cAddress` | nvarchar(100) |  |  |  |  | 税务登记地址 |
| `cEmail` | varchar(50) |  |  |  |  | 电子邮箱 |
| `cTel` | varchar(50) |  |  |  |  | 联系人手机号 |
| `cBank` | nvarchar(30) |  |  |  |  | 开户行 |
| `cAccount` | nvarchar(30) |  |  |  |  | 开户账号 |
| `CreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `cCompanyAddress` | nvarchar(100) |  |  |  |  | 发票邮寄地址 |
| `SignInvoice` | varchar(200) |  |  | 否 | '' | 专票提醒确认函 |
| `isSignInvoice` | tinyint |  |  | 否 | 0 | 是否已签章，0：否，1：是 |
| `cTaxPayerNo` | varchar(50) |  |  |  |  |  |
| `fIsZzsTaxPayer` | tinyint |  |  |  | 1 |  |
| `cTaxPayerFile` | varchar(200) |  |  |  | NULL |  |

## T_PProduct_SupervisePRCEnInsurance

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cSuperviseCode` | nvarchar(50) |  |  |  |  | 监管机构编码 |
| `cSuperviseFullName` | nvarchar(50) |  |  |  |  | 监管机构全称 |
| `cSuperviseName` | nvarchar(50) |  |  |  |  | 监管机构简称 |
| `fSuperviseType` | tinyint |  |  |  |  | 监管机构类型 1市级行政机构 2区县行政机构 |
| `cCityFullName` | nvarchar(50) |  |  |  |  | 监管机构所在地 |
| `cPlatformProvince` | nvarchar(50) |  |  |  |  | 监管机构所在省编码 |
| `cPlatformCity` | nvarchar(50) |  |  |  |  | 监管机构所在市编码 |
| `cPlatformCounty` | nvarchar(50) |  |  |  |  | 监管机构所在县编码 |
| `cName` | nvarchar(50) |  |  |  |  | 监管机构联系人姓名 |
| `cPhone` | nvarchar(50) |  |  |  |  | 监管机构联系人手机 |
| `fModeID` | int |  |  |  |  | 关联到T_PProduct_SuperviseMode ID |
| `cRuleName` | nvarchar(200) |  |  |  |  | 现金保证金监管账户名称规则 |
| `cOnlineFlowCharUrl` | nvarchar(200) |  |  |  |  | 线上出单流程图 |
| `cOfflineFlowCharUrl` | nvarchar(200) |  |  |  |  | 线下办理流程图 |
| `cCoordinate` | varchar(50) |  |  |  |  | 经纬度配置 |
| `cModeName` | nvarchar(200) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cPlatformProvinceCode` | nvarchar(50) |  |  |  |  | 业务渠道所在省编码 |
| `cPlatformCityCode` | nvarchar(50) |  |  |  |  | 业务渠道所在市编码 |
| `cPlatformCountyCode` | nvarchar(50) |  |  |  |  | 业务渠道所在县编码 |
| `fState` | tinyint |  |  | 否 | 0 | 状态 0停用 1启用 |

## T_EnterpriseDiscount_Info

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cEnterpriseName` | nvarchar(50) |  |  | 否 |  |  |
| `cEnterpriseNameCode` | varchar(50) |  |  | 否 |  |  |
| `fPRCEnInsuranceId` | int |  |  | 否 |  |  |
| `fRate` | decimal(10,3) |  |  | 否 |  |  |
| `fMinPremium` | decimal(18,2) |  |  |  |  |  |
| `tStartDate` | datetime |  |  | 否 |  |  |
| `tEndDate` | datetime |  |  | 否 |  |  |
| `tCreateDate` | datetime |  |  |  | getdate() |  |
| `tLastModiftDate` | datetime |  |  |  |  |  |
| `fType` | tinyint |  |  | 否 | 1 |  |
| `cCardId` | varchar(50) |  |  |  |  |  |
| `fAmount` | decimal(18,2) |  |  |  |  |  |
| `fTotalCount` | int |  |  | 否 | 0 |  |
| `fUsedCount` | int |  |  | 否 | 0 |  |
| `fFreezeCount` | int |  |  | 否 | 0 |  |
| `fRestCount` | int |  |  | 否 | 0 |  |

## T_ZX_Banner

*振金Banner表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPosition` | tinyint |  |  | 否 | 0 | 位置 0首页顶部banner、1担保保函顶部、2积分商城顶部、3优惠券底部banner 、4小程序首页弹窗、5【我的】底部、6绑定企业页 |
| `cTitle` | nvarchar(20) |  |  |  |  | 标题 |
| `cDesc` | nvarchar(50) |  |  |  |  | 描述 |
| `cPicUrl` | varchar(200) |  |  |  |  | 图片url |
| `fState` | tinyint |  |  | 否 | 0 | 状态 0 禁用 1 启用 |
| `cJumpUrl` | varchar(200) |  |  |  |  | 跳转链接 |
| `fSort` | int |  |  | 否 | 0 | 排序 数字大靠前 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |
| `fBannerType` | tinyint |  |  | 否 | 0 | 0其他、1抽奖活动 |
| `cBangDingUrl` | varchar(200) |  |  |  |  | 绑定企业页面按钮链接 |

## T_Project_UpdateLog

*项目工程更新日志表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cProjectNo` | varchar(50) |  |  |  |  | 项目编号 |
| `cBidId` | varchar(50) |  |  |  | (0) | 标段ID |
| `fProjectID` | int |  |  |  |  | T_Project_Info表ID |
| `tUpdateTime` | datetime |  |  |  |  | 更改时间 |
| `CreateTime` | datetime |  |  |  | getdate() |  |
| `Prc_id` | int |  |  |  | 0 |  |
| `Insurance_id` | int |  |  | 否 | 0 |  |
| `fGuaranteeCount` | int |  |  | 否 | 0 |  |
| `cAuditUserName` | nvarchar(4) |  |  |  |  |  |
| `fAuditState` | tinyint |  |  | 否 | 0 |  |
| `PrcTypeDB` | varchar(50) |  |  |  |  |  |

## T_PProductYz_CliamTPRecord

*理赔摊赔记录*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `instname` | nvarchar(50) |  |  | 否 |  |  |
| `fStatus` | tinyint |  |  |  | 0 | 状态确认（0：未确认；1：已确认） |
| `fIsMain` | tinyint |  |  |  | 0 | 是否主共记录 |
| `tConfirmTime` | datetime |  |  |  |  | 确认时间 |
| `cUrl` | nvarchar(350) |  |  |  |  | 附件地址 |
| `fCliamId` | int |  |  | 否 |  | 理赔记录id |
| `InsuranceInfoId` | int |  |  | 否 |  | T_PProduct_InsuranceInfo表ID，保司账号所属保司 |
| `tCreateDate` | datetime |  |  |  | getdate() |  |

## T_OnlineInvoice_UserEntVerify

*线上发票-企业认证记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fUserID` | int |  |  | 否 |  | 关联T_OnlineInvoice_User 用户ID |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 企业名 |
| `CreateTime` | datetime |  |  | 否 | getdate() | 认证时间 |
| `cLicenseFile` | varchar(500) |  |  |  |  | 企业授权书 |

## T_Org_PushInfo

*经纪机构数据推送配置表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fType` | tinyint |  |  | 否 | 0 | 0 投标 1 代收 |
| `PRC_id` | int |  |  | 否 | 0 | prcInfo表id |
| `Insurance_id` | int |  |  | 否 | 0 | 金融机构表id |
| `cNumber` | varchar(30) |  |  |  |  | 代收instcode字段值 |
| `appkey` | varchar(50) |  |  | 否 |  |  |
| `appsecret` | varchar(50) |  |  | 否 |  |  |
| `cOrgName` | nvarchar(50) |  |  | 否 |  | 经纪机构名称 |
| `baohannoticeUrl` | varchar(250) |  |  |  |  | 密文推送地址 |
| `kaibiaonoticeUrl` | varchar(250) |  |  |  |  | 明文推送地址 |
| `tuibaonoticeUrl` | varchar(250) |  |  |  |  | 退保推送地址 |
| `fIsPush` | tinyint |  |  | 否 | 1 | 推送开关 0 不推送 1 推送 |
| `tdate` | datetime |  |  | 否 | getdate() | 创建时间 |
| `startday` | date |  |  |  |  | 数据推送的出函起始时间 |
| `fPushType` | tinyint |  |  | 否 | 0 | 推送类型 0默认 推送 承保，开标（一建保） 1 中移推送（代收：出单\开标\退保\退款 投标：开标推送） 2 尚信 (出单\开标\退保) 3 中移java推送（代收：出单\开标\退保\退款 投标：开标推送） |
| `insttype` | varchar(10) |  |  |  |  | 保司代码 PA：平安   HA：华安   GR：国任 |

## T_PProduct_SupervisePRCEnInsuranceInsurance

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fSuperviseEnInsuranceID` | int |  |  |  |  | 类型 1线上 2线下 |
| `fInsuranceID` | int |  |  |  |  | fType=1 对应T_PProduct_InvoiceInfo表ID fType=2 对应T_PProduct_OfflineInsuranceInfo ID |
| `fType` | int |  |  |  |  | 类型 1线上 2线下 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cName` | nvarchar(50) |  |  |  |  |  |
| `cPhone` | nvarchar(50) |  |  |  |  |  |
| `cCustomerServicePhone` | nvarchar(50) |  |  |  |  |  |
| `cPRCCode` | nvarchar(50) |  |  |  |  |  |

## T_EnterpriseDiscount_Log

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cUser` | nvarchar(10) |  |  |  |  |  |
| `cOperation` | nvarchar(50) |  |  |  |  |  |
| `cOperationContent` | nvarchar(1000) |  |  |  |  |  |
| `cRemark` | nvarchar(1000) |  |  |  |  |  |
| `cFileUrls` | varchar(500) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  | getdate() |  |
| `fEnterpriseDiscountId` | int |  |  | 否 |  |  |
| `fImportLogId` | int |  |  |  |  |  |

## T_tsign_updateLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `OrganizeAccountId` | nvarchar(50) |  |  |  |  | e签宝用户ID |
| `oldName` | nvarchar(50) |  |  |  |  | 原企业名称 |
| `newName` | nvarchar(50) |  |  |  |  | 修改后企业名称 |
| `createTime` | datetime |  |  |  | getdate() |  |
| `modifySource` | nvarchar(25) |  |  |  |  | 修改来源 |

## T_PProduct_GuaranteeCargoStandardList

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(50) |  |  | 否 |  |  |
| `cStandard` | nvarchar(50) |  |  | 否 |  |  |
| `fCount` | nvarchar(50) |  |  | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  | 否 |  |  |

## T_PRC_ApiUrl

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `platformcode` | varchar(50) | 是 |  | 否 |  |  |
| `InsuranceName` | nvarchar(50) | 是 |  | 否 |  |  |
| `baohannoticeUrl` | varchar(200) |  |  |  |  |  |
| `restorenoticeUrl` | varchar(200) |  |  |  |  |  |
| `invoicenoticeUrl` | varchar(200) |  |  |  |  |  |
| `quitnoticeUrl` | varchar(200) |  |  |  |  |  |
| `tdate` | datetime |  |  | 否 | getdate() |  |
| `cancelnoticeUrl` | varchar(200) |  |  |  |  |  |
| `quitbohuiUrl` | varchar(200) |  |  |  |  |  |
| `claimsnoticeUrl` | varchar(200) |  |  |  |  |  |
| `claimsrepaynoticeUrl` | varchar(200) |  |  |  |  | 理赔追偿推送 |
| `claimsPushState` | varchar(50) |  |  |  |  | 理赔哪些状态需要推送，如3,5 |
| `claimsReportFileState` | varchar(50) |  |  |  |  | 理赔哪些状态需要推送文件，如3 |
| `topaynoticeUrl` | varchar(200) |  |  |  |  |  |
| `paidnoticeUrl` | varchar(200) |  |  |  |  |  |

## T_VoiceNotice_Task

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cTaskCode` | varchar(50) |  |  | 否 |  |  |
| `fTemplateType` | tinyint |  |  | 否 | 0 | 模板类型 1语音文本转语音模板 2语音文件模板 |
| `fTemplateID` | int |  |  | 否 | 0 | 模板id |
| `fCallType` | tinyint |  |  | 否 | 0 | 外呼类型（1：公共模式；2：专属模式） |
| `cCallTel` | varchar(20) |  |  |  |  | 专属模式时填写外呼号码 |
| `fState` | tinyint |  |  | 否 | 0 | 状态 0未开始 1进行中 2已完成 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `tStartTime` | datetime |  |  |  |  |  |
| `tEndTime` | datetime |  |  |  |  | 任务结束时间 |

## T_PProduct_SupervisePRCRelation

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCID` | int |  |  |  |  |  |
| `fSuperviseOrganID` | int |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  |  |  |

## T_ZX_PrizeRecord

*振鑫-奖品记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fZXUserID` | int |  |  |  | 0 | 关联T_ZX_User表ID |
| `fPrizeId` | int |  |  |  | 0 | 关联T_ZX_PrizeConfigs表ID |
| `cPrizeName` | nvarchar(20) |  |  |  |  | 奖品名称 |
| `fPrizeAmount` | decimal(10,2) |  |  |  |  | 奖品金额，单位：元 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `cIpAddress` | varchar(50) |  |  |  |  | IP地址 |
| `cUserAgent` | varchar(200) |  |  |  |  | User-Agent |
| `fTag` | int |  |  |  | 0 | 活动标签，值1：618 新人注册抽奖活动 |
| `fStatus` | tinyint |  |  |  | 0 | 奖品状态，0待发放，1待领取，2用户取消，3领取成功，4失败，5后台重置 |
| `tSendTime` | datetime |  |  |  |  | 奖品发放时间（弹窗领取确认页的时间） |
| `cOutOpenid` | varchar(50) |  |  |  |  | 用户在第三方的openid |
| `fOrderId` | int |  |  |  |  | 第三方订单请求记录id |

## T_Epoint_Guarantee_tb

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `applyno` | varchar(50) | 是 |  | 否 |  | 保函编号 |
| `platformname` | nvarchar(50) |  |  | 否 |  | 平台名称 |
| `unitname` | nvarchar(50) |  |  | 否 |  | 出函机构 |
| `danweiname` | nvarchar(200) |  |  | 否 |  | 投标企业单位名称 |
| `orgnum` | varchar(200) |  |  | 否 |  | 投标人信用代码 |
| `contactperson` | nvarchar(200) |  |  | 否 |  | 投标单位联系人 |
| `contactphone` | varchar(200) |  |  | 否 |  | 投标单位联系方式 |
| `baofei` | decimal(18,2) |  |  | 否 |  | 保费金额 |
| `bzjamount` | decimal(18,2) |  |  | 否 |  | 保证金金额 |
| `successdate` | datetime |  |  |  |  | 出函时间 |
| `kaibiaotime` | datetime |  |  | 否 |  | 开标时间 |
| `biaoduanno` | varchar(200) |  |  | 否 |  | 标段编号 |
| `biaoduanname` | nvarchar(200) |  |  | 否 |  | 标段名称 |
| `zbr` | nvarchar(200) |  |  | 否 |  | 招标人 |
| `zbrorgnum` | nvarchar(200) |  |  | 否 |  | 招标人统一社会信用代码 |
| `tdate` | datetime |  |  | 否 | getdate() | 入库时间 |
| `baohanno` | varchar(50) |  |  |  |  |  |
| `referralcode` | nvarchar(50) |  |  |  |  |  |
| `issuccess` | nvarchar(10) |  |  | 否 | '' |  |

## T_PProductYz_UserPRCEnInsurance

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCEnInsuranceId` | int |  |  | 否 |  |  |
| `fUserId` | int |  |  | 否 |  |  |
| `tCreateTime` | datetime |  |  |  |  |  |

## T_PProduct_GuaranteeDelayRecord

*保单延期记录*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  |  |  |  |
| `cOldPolicyUrl` | nvarchar(300) |  |  |  |  | 旧保单（做备份） |
| `cNewPolicyUrl` | nvarchar(300) |  |  |  |  | 新保单 |
| `tNewEndDate` | datetime |  |  |  |  | 新的保单结束时间 |
| `tCreateDate` | datetime |  |  |  |  | 操作时间 |
| `cCreateUser` | nvarchar(50) |  |  |  |  | 操作人 |
| `tOldEndDate` | datetime |  |  |  |  | 保单原止期 |

## T_PProductWarn_Insurance

*农民工工资支付监控平台-金融机构基本信息*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fType` | tinyint |  |  |  | 1 | 金融机构类型1 银行 2 保险公司 |
| `cParentCode` | varchar(20) |  |  |  |  | 父级银行类型Code |
| `cCode` | varchar(20) |  |  |  |  | 子级银行类型Code |
| `cBankName` | nvarchar(50) |  |  |  |  | 银行名称 |
| `cBranchName` | nvarchar(50) |  |  |  |  | 支行名称 |
| `cBankNo` | varchar(20) |  |  |  |  | 银行联号 |
| `fPushState` | tinyint |  |  |  | 0 | 状态 （0：备案中；1：已备案；2：备案失败） |
| `cErrorMsg` | nvarchar(100) |  |  |  |  | 备案结果 |
| `cPRCCode` | nvarchar(50) |  |  |  |  | 业务渠道编码 |
| `tCreateTime` | datetime |  |  |  |  | 创建时间 |

## T_OnlineInvoice_QueryEntParam

*用户有效检索参数*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fUserID` | int |  |  | 否 |  | 关联T_OnlineInvoice_User 用户ID |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 企业名 |
| `cRealName` | nvarchar(50) |  |  |  |  | 经办人 |
| `cPhone` | nvarchar(50) |  |  |  |  | 联系方式 |
| `CreateTime` | datetime |  |  | 否 | getdate() |  |
| `DataSource` | tinyint |  |  | 否 | 1 |  |

## T_zk_interface

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `Prc_id` | int |  |  |  |  | T_PRC_Info.ID |
| `Insurance_id` | int |  |  |  |  | T_Insurance_Info.ID |
| `CdUrl` | varchar(200) |  |  |  |  | 出单地址 |
| `PdUrl` | varchar(200) |  |  |  |  | 批单地址 |
| `FpUrl` | varchar(200) |  |  |  |  | 发票地址 |
| `DdgbUrl` | varchar(200) |  |  |  |  | 订单关闭地址 |
| `CdztcxUrl` | varchar(200) |  |  |  |  | 出单状态查询url |
| `TbUrl` | varchar(200) |  |  |  |  | 退保地址 |
| `Api` | varchar(200) |  |  |  |  | 保司出单参数 |
| `appkey` | varchar(200) |  |  |  |  |  |
| `appsecret` | varchar(200) |  |  |  |  |  |
| `OSS_Url` | varchar(200) |  |  |  |  | OOS前缀地址 |
| `FileAddree` | varchar(200) |  |  |  |  | 文件存储系统接口 |
| `Remarks` | varchar(200) |  |  |  |  | 备注说明 |
| `CustomCode` | nvarchar(200) |  |  |  |  | 定制脚本标识 |
| `interceptCheckDateUrl` | nvarchar(200) |  |  |  |  | 拦截检查日期 开标前一个工作日，不是自然日校验(李委提供的方法) |
| `interceptcheckDateEnable` | nvarchar(10) |  |  |  |  | 拦截检查日期是否启用 0 启用,1关闭   正式库设置为0;测试库设置为1 绕过校验 |
| `xxjyUrl` | nvarchar(200) |  |  |  |  | 信息校验接口 |
| `FpztcxUrl` | varchar(200) |  |  |  |  | 发票状态查询地址(部分地区开票结果需要主动轮询获得) |
| `MyPublicKey` | nvarchar(1000) |  |  |  |  | 我方公钥 |
| `MyPrivateKey` | nvarchar(MAX) |  |  |  |  | 我方私钥 |
| `CounterpartyPublicKey` | nvarchar(1000) |  |  |  |  | 对接方公钥 |

## T_VoiceNotice_TaskLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fTaskID` | int |  |  | 否 | 0 | 任务id |
| `cPhone` | varchar(20) |  |  | 否 |  | 被叫号码 |
| `fType` | tinyint |  |  | 否 | 0 | 类型 0 成功 1 失败 |
| `cMessage` | nvarchar(200) |  |  |  |  | 错误 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_PProduct_SuperviseRule

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fSupervisePRCEnInsuranceID` | int |  |  |  |  | 关联机构ID T_PProduct_SupervisePRCEnInsurance |
| `fSGContractAmountMin` | decimal(18,2) |  |  |  |  | 施工合同金额最小值(元) |
| `fSGContractAmountMax` | decimal(18,2) |  |  |  |  | 施工合同金额最大值(元) |
| `fSGContractAmountType` | tinyint |  |  |  |  | 施工合同金额范围类型 |
| `fRate` | decimal(18,4) |  |  |  |  | 费率 |
| `fMarginAmountMax` | decimal(18,2) |  |  |  |  | 最高保证金金额(元) |

## T_Epoint_Interface

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Prc_id` | int | 是 |  | 否 |  | T_Prc_Info表id |
| `AppKey` | varchar(50) |  |  | 否 |  | appkey |
| `AppSecret` | varchar(64) |  |  | 否 |  | appsecret |
| `cKey` | varchar(40) |  |  |  |  | sm4的密钥key |
| `cIv` | varchar(40) |  |  |  |  | sm4的子秘钥iv |
| `baohannoticeUrl` | varchar(200) |  |  |  |  | 保函通知url |
| `uploadbaohanfileUrl` | varchar(200) |  |  |  |  | 上传保函url |
| `downloadpublickeyUrl` | varchar(200) |  |  |  |  | 下载sm2公钥 |
| `baohanfilecompletenoticeUrl` | varchar(200) |  |  |  |  | 保函上传完成通知url |
| `invoicenoticeUrl` | varchar(200) |  |  |  |  | 发票通知url |
| `quitnoticeUrl` | varchar(200) |  |  |  |  | 退保通知url |
| `ofdhandlerUrl` | varchar(200) |  |  |  |  |  |
| `fIsRedirectUrl` | tinyint |  |  | 否 | 0 |  |
| `PrcCodeSuffix` | varchar(10) |  |  |  |  |  |
| `fState` | tinyint |  |  | 否 | 2 |  |
| `cancelUrl` | varchar(200) |  |  |  |  |  |
| `checkbasicaccountUrl` | varchar(200) |  |  |  |  |  |
| `downloadUrl` | varchar(200) |  |  |  |  |  |
| `kaibiaoquitnoticeUrl` | varchar(200) |  |  |  |  |  |
| `quittimeUrl` | varchar(200) |  |  |  |  |  |
| `claimsresultnoticeUrl` | varchar(200) |  |  |  |  |  |
| `checkkaibiaoUrl` | varchar(200) |  |  |  |  | 校验是否开标接口地址 |
| `isUploadfirst` | tinyint |  |  | 否 | 0 | 保函通知时是否先调用上传文件接口 0 否 1 是 |
| `checkbasicaccountUrlv2` | varchar(200) |  |  |  |  | 新的基本户校验接口，无打款时间，无生效时间，有平台编码字段 |
| `isInvoiceUpload` | tinyint |  |  | 否 | 0 |  |
| `claimsrepaynoticeUrl` | varchar(200) |  |  |  |  |  |
| `cDecryptkey` | varchar(30) |  |  |  |  | 解密申请接口里项目信息的key，新点提供固定的(泸州模式) |
| `giveupnoticeUrl` | varchar(200) |  |  |  |  |  |

## T_XK_Contacts_DataStatisticsRule

*线客联系人出单数据监测规则表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cType` | varchar(50) |  |  |  |  | 规则名称 |
| `cRule` | varchar(500) |  |  |  |  | 预警规则JSON形式存放 |

## T_GzZrx_DataPermissionsPRC

*雇主责任险-数据权限与二级渠道关系表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Id` | varchar(50) | 是 |  | 否 |  |  |
| `cDataPermissionsID` | varchar(50) |  |  | 否 |  | 数据权限ID，T_GzZrx_DataPermissions表ID |
| `fChannelID` | int |  |  | 否 | 0 | 一级渠道ID |
| `fPRCID` | int |  |  | 否 | 0 | 二级渠道ID |
| `tCreateTime` | datetime |  |  | 否 |  | 创建时间 |

## T_Pay_Log

*支付记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `transno` | varchar(50) | 是 |  | 否 |  | 银行流水号 |
| `transtime` | datetime |  |  | 否 |  | 支付时间 |
| `transamount` | decimal(18,2) |  |  | 否 |  | 支付金额 |
| `payeracctno` | varchar(50) |  |  | 否 |  | 付款卡号 |
| `payeracctname` | nvarchar(50) |  |  | 否 |  | 付款户名 |
| `abstractinfo` | nvarchar(50) |  |  |  |  | 备注 |
| `oppositebankno` | varchar(50) |  |  | 否 |  | 付款行号 |
| `oppositebankname` | nvarchar(50) |  |  | 否 |  | 付款行名 |
| `tdate` | datetime |  |  | 否 | getdate() | 日期 |
| `OrderNo` | varchar(50) |  |  |  |  | 订单号 |
| `fState` | tinyint |  |  | 否 | 0 | 0:未使用，1：已使用，2：退款中，3：已退款 |
| `cardType` | tinyint |  |  | 否 | 0 | 付款卡归属，去T_pay_log_cardType表里查TypeNo字段说明 |
| `TimeStab` | varchar(50) |  |  |  |  |  |
| `transtdate` | date |  |  |  |  |  |
| `cAuditMessage` | nvarchar(100) |  |  |  |  |  |
| `cAuditUserName` | nvarchar(50) |  |  |  |  |  |
| `cAuditTime` | datetime |  |  |  |  |  |
| `skAccount` | varchar(50) |  |  | 否 |  |  |
| `fState_tk` | tinyint |  |  | 否 | 0 | 默认0未出函退款，1注销退款，2保司退保退款 |
| `fChkPremium` | decimal(10,2) |  |  |  |  | 支付金额与保费不一致时，赋值保费 |
| `ReceiptUrl` | varchar(500) |  |  |  |  | 银行回单地址 |
| `ftkIsPush` | tinyint |  |  | 否 | 0 | 机构未函退款推送：0未推送 1已推送 |

## T_PProduct_GuaranteeDelayRecordApply

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  |  |  |  |
| `cFileUrl` | nvarchar(300) |  |  |  |  | 延期证明文件 |
| `tEndDate` | datetime |  |  |  |  | 工程止期 |
| `tCreateDate` | datetime |  |  |  |  | 操作时间 |
| `cCreateUser` | nvarchar(50) |  |  |  |  | 操作人 |
| `fStatus` | int |  |  |  | 0 | 状态 0：待保司处理；1：已处理 |
| `tAuthDate` | datetime |  |  |  |  | 延保时间（保司） |
| `cAuthUser` | nvarchar(50) |  |  |  |  | 延保操作人（保司） |

## T_ZX_EquityCouponGroup

*权益优惠券组表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEquityID` | int |  |  | 否 | 0 | 权益表ID |
| `cGroupCode` | varchar(50) |  |  | 否 |  | 优惠券组编码 |
| `cGroupName` | nvarchar(50) |  |  |  |  | 优惠券组名称 |
| `fState` | tinyint |  |  | 否 | 0 | 状态 0禁用 1启用 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_VoiceNotice_TaskPhone

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fTaskID` | int |  |  | 否 |  |  |
| `cPhone` | varchar(20) |  |  | 否 |  |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_PProduct_Surrender

*履约申请退保、关闭订单记录*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  | 关联企业表ID |
| `fGuaranteeInfoID` | int |  |  |  |  | 关联订单表ID |
| `CreateTime` | datetime |  |  |  | getdate() |  |
| `fState` | tinyint |  |  |  | 0 | 0默认申请，关闭订单原订单状态值 |
| `cFileUrl` | varchar(250) |  |  |  |  | 申请书 |
| `tGetFileTime` | datetime |  |  |  |  |  |
| `fType` | tinyint |  |  |  | 0 | 默认0退保，1关闭订单 |

## T_Epoint_InterfaceExtend

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `platformcode` | varchar(50) |  |  | 否 |  |  |
| `insttype` | varchar(20) |  |  |  |  |  |
| `appkey` | varchar(50) |  |  | 否 |  |  |
| `PrcCodeSuffix` | varchar(10) |  |  |  |  |  |
| `fType` | tinyint |  |  | 否 | 0 |  |

## T_ZX_Channel

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cChannelCode` | varchar(50) |  |  | 否 |  | 一级渠道编码 |
| `cChannelName` | nvarchar(50) |  |  | 否 |  | 一级渠道名称 |
| `cChannelShortName` | nvarchar(20) |  |  |  |  | 一级渠道简称 |
| `cAttributionUser` | nvarchar(10) |  |  |  |  | 业务归属 |
| `cQrCodeUrl` | varchar(200) |  |  |  |  | 二维码 |
| `fState` | tinyint |  |  | 否 | 0 | 状态 0禁用1启用 |
| `cRemark` | nvarchar(200) |  |  |  |  | 备注 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |
| `cQiWeiUrl` | varchar(200) |  |  |  |  | 企微图片 |

## T_Relation_PRCEnInsuranceUserAcct

*易联请求参数设置表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `fPRCEnInsuranceID` | int | 是 |  | 否 | 0 | 对应T_Relation_PRCEnInsurance表ID |
| `userAcct` | varchar(30) |  |  |  |  | 配置账号 |
| `password` | varchar(30) |  |  |  |  | 配置密码 |
| `productCode` | varchar(30) |  |  |  |  | 易联方案代码 |
| `programCode` | varchar(30) |  |  |  |  | 易联对接编号 |
| `projectCode` | varchar(30) |  |  |  |  | 易联项目编码 |
| `invoice_merchantNo` | varchar(30) |  |  |  |  | 商户号(请求来源） |
| `invoice_qudao` | varchar(30) |  |  |  |  | 发票渠道标识 |
| `invoice_md5Salt` | varchar(30) |  |  |  |  | 发票md5加盐 |
| `pigai_loginName` | varchar(30) |  |  |  |  | 批改登录名 |
| `pigai_jointBusinessCode` | varchar(30) |  |  |  |  | 批改渠道来源 |
| `pigai_actual_productCode` | varchar(30) |  |  |  |  | 批改险种代码 |
| `fState` | tinyint |  |  |  | 0 | 状态，0禁用，1启用 |
| `yewulaiyuan` | varchar(30) |  |  |  |  | 业务来源 |
| `chudanyuan` | varchar(30) |  |  |  |  | 出单员代码 |
| `zhidanjigou` | varchar(30) |  |  |  |  | 制单机构（出单员归属机构） |
| `yewuyuan` | varchar(30) |  |  |  |  | 业务员代码 |
| `yewuyuanjigou` | varchar(30) |  |  |  |  | 业务归属机构代码（业务员的归属机构） |
| `hebaoyuan` | varchar(30) |  |  |  |  | 核保员代码 |
| `dailiren` | varchar(30) |  |  |  |  | 代理人代码 |
| `dailirenxieyi` | varchar(30) |  |  |  |  | 代理人协议号 |
| `shouxvfei` | varchar(10) |  |  |  | (0) | 手续费比例 |
| `yingxiaoqudao` | varchar(30) |  |  |  |  | 营销渠道 |
| `qixian` | varchar(10) |  |  |  |  | 保险期限（单位：月） |
| `danzhengleixing` | varchar(10) |  |  |  |  | 单证类型（凭证类型），100表示不输出凭证 |
| `zhugongbao` | tinyint |  |  |  | 0 | 是否主共保，默认0否，1是 |
| `ofd` | tinyint |  |  |  | 0 | 是否OFD，默认0否，1是 |
| `invoice_downApiUrl` | varchar(200) |  |  |  |  | 发票下载接口地址 |
| `cSheng` | nvarchar(10) |  |  |  |  | 省份 |
| `cInsuranceLogoUrl` | varchar(500) |  |  |  |  | 机构LOGO地址 |
| `cPartnerName` | varchar(100) |  |  |  |  | 合作机构名称 |
| `cApiParametersPush` | varchar(3000) |  |  |  |  | 接口参数拼接 |
| `evisePolicyApiUrl` | varchar(100) |  |  |  |  | 机构批改接口地址 |
| `fIsGetXiaoShouXinXi` | tinyint |  |  | 否 | 1 | 是否传传销售信息，1是，0否 |
| `isChangebidStartTime` | tinyint |  |  | 否 | 1 | 是否要修改保险起止日期，1是 |
| `clauseCode` | varchar(30) |  |  |  |  | 机构条款代码 |
| `fIsGetFuJiaXian` | tinyint |  |  | 否 | 0 | 是否带有附加险，1是 |
| `fUseBidName` | tinyint |  |  | 否 | 0 | 是否用标段名称来代替项目名称，1是 |
| `cRemarks` | nvarchar(50) |  |  |  |  | 备注 |
| `downPolicyOFDApiUrl` | varchar(100) |  |  |  |  | 下载OFD接口地址 |
| `invoice_appApiUrl` | varchar(100) |  |  |  |  | 发票申请接口地址 |
| `greetingApiUrl` | varchar(100) |  |  |  |  | 承保接口地址 |
| `fIsImmediate` | tinyint |  |  | 否 | 0 | 是否即时起保，1是，2（宜宾）tender_start_time字段0时为起保，3（德阳）bzjenddate_encryption为起保，4第2天0时起保，22tender_start_time起保，大于等于值5，作为延迟几分钟，22（玉环）tender_start_time字段为起保 |
| `fisChangebidStartTimeType` | tinyint |  |  | 否 | 0 | 标的日期启用类型，0出单后第2天0点，1开标时间当天（格式"yyyy-MM-dd 00:00:00"），2开标时间当天（格式2005-11-05T14:30:00.000+0800） |
| `fEndorRequestType` | tinyint |  |  | 否 | 13 | 批改次数，13一次批改，25三次批改 |
| `claimsSettlementChannel` | varchar(20) |  |  |  |  | 是否开通理赔绿色通道的字段,0否 |
| `fStartAddCountTime` | int |  |  | 否 | 1 | 没有开标时间的话，第2天0点起保，即出单时间加上的天数 |
| `regionCode` | varchar(20) |  |  |  |  | 区域码，老核心下载OFD有用到 |
| `cBusinessId` | varchar(20) |  |  |  |  | 立项编码，值999时招标文件编号 |
| `cMobileMsg` | varchar(20) |  |  |  |  | 值1| 发出函短信通知 |
| `policySurrenderApiUrl` | varchar(100) |  |  |  |  | 退保接口地址 |
| `frequency` | tinyint |  |  |  |  | 1、批改后不需要拼接，2、批改在原ofd的文件上拼接一个新的ofd文件 |
| `identifyNumber` | varchar(20) |  |  |  |  | 加密保单上显示的投保人代码，为空则显示999999 |
| `fJoin` | tinyint |  |  | 否 | 0 | 1、广安拼接模式，项目名称=项目名称(标段名称)，项目编号=项目编号(标段编号)；2、宜宾模式，3、郴州OFD模式，4、广元模式，5、绵阳模式，6、内蒙模式 |
| `cSurrenderCode` | varchar(50) |  |  |  |  | 退保附加条款的编号，目前郴州 |
| `cPushCentralApi` | varchar(350) |  |  |  |  | 调用推送中心接口 |
| `cFuJiaXianCode` | varchar(30) |  |  |  |  | 附加险码 |
| `fEncryption` | tinyint |  |  | 否 | 0 | 保单里字段加密类型，0不加密，1通过SM4加密，2绵阳 |
| `fAttachmentType` | tinyint |  |  | 否 | 0 | 传附件模式，默认0无，1湖州下载OFD接口里传《投保单》签章文件，2（内蒙）、3（广元）、4（绵阳） |
| `file_uploadApiUrl` | varchar(100) |  |  |  |  | 影像上传接口地址 |
| `underlineQueryApiUrl` | varchar(100) |  |  |  |  | 线下转账查询接口 |
| `fFieldSaveType` | tinyint |  |  |  | 0 | 保存值类型，1和31（insuranceStartDate，insuranceEndDate），2（fMainCo=1） |
| `fChkJiBenHu` | tinyint |  |  | 否 | 1 | 请求保司接口，是否要验证基本户信息，默认1是，0否 |
| `policyQueryApiUrl` | varchar(100) |  |  |  |  | 保函查询接口 |

## T_PProduct_GuaranteeEditLog

*编辑订单字段信息记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  |  |  |  |
| `cTag` | nvarchar(20) |  |  |  |  | 修改标签类型 |
| `cFieldNameBz` | nvarchar(20) |  |  |  |  | 字段名备注 |
| `cFieldName` | varchar(30) |  |  |  |  | 字段名 |
| `cOldValue` | varchar(3000) |  |  |  |  | 变更前内容 |
| `cNewValue` | varchar(3000) |  |  |  |  | 变更后内容 |
| `fIsJson` | tinyint |  |  |  | 0 | 变更内容是否是JSON存储，默认0否，1是，区分cOldValue和cNewValue，2是，cNewValue里记录新旧值 |
| `cAuditNotes` | nvarchar(300) |  |  |  |  | 备注 |
| `cAuditUserName` | nvarchar(20) |  |  |  |  | 操作人 |
| `CreateTime` | datetime |  |  |  |  |  |
| `fIsCheck` | tinyint |  |  | 否 | 0 | 是否查看 0 否 1 是 |
| `tCheckTime` | datetime |  |  |  |  | 查看时间 |

## T_PProduct_Guarantee_Protocol

*商城增信-协议表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fGuaranteeId` | int |  |  | 否 |  | 关联订单id |
| `cProtocolId` | varchar(20) |  |  | 否 |  | 协议id |
| `cProtocolNo` | nvarchar(50) |  |  |  |  | 协议编号 |
| `cProtocolName` | nvarchar(100) |  |  |  |  | 协议名称 |
| `cProtocolUrl` | nvarchar(MAX) |  |  |  |  | 协议附件列表，目前没用到，只做存储记录 |
| `tCreateTime` | datetime |  |  |  | getdate() |  |

## T_VoiceNotice_TaskPhoneVariable

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fTaskID` | int |  |  | 否 |  | 任务号码id |
| `cPhone` | varchar(20) |  |  | 否 |  |  |
| `cVariableName` | varchar(50) |  |  | 否 |  | 变量名称 |
| `cVariableValue` | nvarchar(150) |  |  |  |  | 变量值 |

## T_PProduct_tsignAuthentication

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  | 否 |  | 企业ID |
| `cEnterpriseName` | nvarchar(50) |  |  | 否 |  | 企业名称 |
| `cBank` | nvarchar(50) |  |  |  |  |  |
| `cBankCardNo` | varchar(50) |  |  | 否 |  | 基本户帐号 |
| `amount` | decimal(10,2) |  |  | 否 |  | 随机金额 |
| `fstate` | tinyint |  |  | 否 | 0 | 认证状态，0：未认证，1：已认证 |
| `fpayId` | int |  |  |  |  | 付款记录表ID |
| `cBankVoucher` | varchar(200) |  |  |  |  |  |
| `tUpTime` | datetime |  |  |  |  |  |
| `type` | tinyint |  |  |  | 0 | 渠道类型（0默认，1线下） |

## T_PProduct_GuaranteeEnAttachment

*农民工履约保单附件表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `fGuaranteeID` | int |  |  |  |  |  |
| `fEnterpriseAttachmentID` | int |  |  |  |  |  |
| `CreateTime` | datetime |  |  |  |  |  |
| `fImageIsPush` | tinyint |  |  |  |  | 推送影像文件，0:未推送 2：未打包，4：已打包，6：已推送 |

## T_ExportTemplate_Log

*运维导出历史记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cBusinessTag` | tinyint |  |  |  | 0 | 业务类型，默认0投标业务，1基本户业务 |
| `CreateTime` | datetime |  |  |  |  |  |
| `platformcode` | varchar(3000) |  |  |  |  | 中心 |
| `cInsuranceCompany` | varchar(300) |  |  |  |  | 保险公司 |
| `cBidTime` | varchar(100) |  |  |  |  | 开标时间区间 |
| `cFileUrl` | varchar(300) |  |  |  |  | 文件地址 |
| `cType` | nvarchar(20) |  |  |  |  | 模板类型 |
| `cAuditUserName` | nvarchar(20) |  |  |  |  | 导出人员 |
| `cPolicyTime` | varchar(100) |  |  |  |  |  |
| `cAusers` | nvarchar(50) |  |  |  |  |  |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  |  |
| `cState` | nvarchar(50) |  |  |  |  |  |
| `cBidName` | nvarchar(100) |  |  |  |  |  |
| `fMarginAmount` | decimal(18,2) |  |  | 否 | 0 |  |
| `fPremium` | decimal(18,2) |  |  | 否 | 0 |  |
| `fIsOpen` | tinyint |  |  | 否 | 1 |  |
| `fExportState` | tinyint |  |  | 否 | 1 | 导出状态，1已导出，0未导出，2已取消导出 |
| `tExportTime` | datetime |  |  |  |  | 导出时间，导出状态是1时，导出时间同创建时间CreateTime |
| `fExportType` | int |  |  | 否 | 0 |  |
| `cErrorInfor` | nvarchar(500) |  |  |  |  |  |

## T_ZX_PrizeConfigs

*振鑫-奖品配置表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(20) |  |  |  |  | 奖品名称 |
| `fAmount` | decimal(10,2) |  |  |  | 0 | 金额，单位：元 |
| `fProbability` | decimal(10,2) |  |  |  | 0 | 中奖概率 |
| `fAngle` | int |  |  |  | 0 | 角度 |
| `fMaxDailyCount` | int |  |  |  | 0 | 当天最大次数 |
| `fIsDefault` | tinyint |  |  |  | 0 | 是否默认 |
| `fIsDelete` | tinyint |  |  |  | 0 | 是否删除，1是，0否 |

## T_PProduct_PRCEnInsuranceBusiManager

*客户经理信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(50) |  |  | 否 |  | 客户经理 |
| `fPRCEnInsuranceID` | int |  |  | 否 |  | T_PProduct_PRCEnInsurance 表id |
| `tCreateDate` | datetime |  |  |  | getdate() |  |

## T_GzZrx_GuaranteeMain

*主订单表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cMainNo` | nvarchar(50) |  |  |  |  | 主订单表编号 |
| `cProductName` | nvarchar(50) |  |  |  |  | 保险产品 |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 企业名称 |
| `cEnterpriseNameCode` | nvarchar(32) |  |  |  |  | 统一社会信用代码 |
| `cBank` | nvarchar(50) |  |  |  |  | 基本户开户行 |
| `cBankCardNo` | varchar(50) |  |  |  |  | 基本户账号 |
| `cRealName` | nvarchar(50) |  |  |  |  | 联系人姓名 |
| `cPhone` | nvarchar(50) |  |  |  |  | 联系人手机号码 |
| `fMarginAmount` | decimal(18,2) |  |  | 否 | 0 | 保证金金额 |
| `fPrcEnsuranceId` | int |  |  | 否 | 0 | 平台id  T_GzZrx_PRCInsurance |
| `cInsuranceCompany` | nvarchar(50) |  |  |  |  | 保险公司名称 |
| `cInsuranceTypeNo` | varchar(50) |  |  |  |  | 险种编码，关联T_GzZrx_Insurance表cProNo |
| `fPackageId` | int |  |  |  |  | 套餐方案id  (T_GzZrx_Package) |
| `cPackageCode` | varchar(50) |  |  |  |  | T_GzZrx_Package编码 |
| `provinceName` | nvarchar(20) |  |  |  |  | 省 |
| `cityName` | nvarchar(20) |  |  |  |  | 市 |
| `areaName` | nvarchar(20) |  |  |  |  | 区 |
| `provinceCode` | nvarchar(20) |  |  |  |  |  |
| `cityCode` | nvarchar(20) |  |  |  |  |  |
| `areaCode` | nvarchar(20) |  |  |  |  |  |
| `cOwner` | nvarchar(50) |  |  |  |  | 被保险人 |
| `cOwnerCode` | nvarchar(32) |  |  |  |  | 被保险人信用代码 |
| `fBusinessType` | nvarchar(20) |  |  |  |  | 行业代码 |
| `fPremium` | decimal(18,2) |  |  |  | 0 | 保费(元) |
| `cPolicyNo` | nvarchar(50) |  |  |  |  | 人保保单号 |
| `cPolicyUrl` | varchar(500) |  |  |  |  | 人保保单下载地址 |
| `cPolicyLocalUrl` | varchar(500) |  |  |  |  | 人保保单本地地址 |
| `tReceivePolicyTime` | datetime |  |  |  |  | 人保保单接收时间 |
| `tPolicyTime` | datetime |  |  |  |  | 人保保单生成时间 |
| `tGuaranteedTime` | datetime |  |  |  |  | 出函时间 |
| `CreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `fTotalEmployeeCount` | int |  |  |  | 0 | 总投保雇员数 |
| `fInsuredChk` | tinyint |  |  |  | 1 | 被保险信息，1同投保人一致，2与投保人不一致 |
| `PRC_id` | int |  |  | 否 | 0 | T_GzZrx_PRC  表id |
| `platformcode` | nvarchar(50) |  |  |  |  | 平台编码（二级渠道编码 对应 T_GzZrx_PRC  code） |
| `fProgrammeId` | int |  |  | 否 | 0 | T_GzZrx_PRCProgramme 表id |
| `cDuration` | nvarchar(10) |  |  |  |  | 期限 |

## T_VoiceNotice_Template

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(50) |  |  | 否 |  | 模板名称 |
| `cCode` | nvarchar(100) |  |  | 否 |  | 模板ID |
| `fType` | tinyint |  |  | 否 | 1 | 模板类型：（1. 文本转语音模板；2. 语音文件模板） |
| `cContent` | nvarchar(500) |  |  | 否 |  | 内容 |
| `fCallType` | tinyint |  |  | 否 | 0 | 外呼类型（0：公共模式；1：专属模式） |
| `tCreateDate` | datetime |  |  | 否 | getdate() | 创建时间 |
| `cCreateUser` | nvarchar(50) |  |  |  |  |  |
| `tLastModifyUser` | nvarchar(50) |  |  |  |  | 最后修改人 |
| `tLastModifyDate` | datetime |  |  |  |  | 最后修改时间 |
| `fIsDelete` | tinyint |  |  |  | 0 | 是否删除（0：否；1：是） |

## T_PProduct_UserProduct

*农民工履约企业所属产品表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  | 0 |  |
| `cProductNo` | varchar(50) |  |  |  |  | 产品序列号 |

## T_Fstate_Order

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `fstate` | tinyint | 是 |  | 否 |  | 状态值 |
| `platformcode` | varchar(50) | 是 |  | 否 |  | 平台码 |
| `name` | nvarchar(20) |  |  |  |  | 状态名称 |
| `orderNum` | tinyint |  |  | 否 | 0 | 排序参数,越大越靠前 |
| `remark` | nvarchar(50) |  |  |  |  |  |

## T_WeekDay_Cache

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `tdate` | date |  |  |  |  | 当前日期 |
| `isworkday` | tinyint |  |  | 否 | 0 | 是否工作日 0否 1是 |

## T_PProductYZ_PRCEnInsurance

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fInsuranceID` | int |  |  | 否 |  | T_PProduct_InsuranceInfo表id |
| `cInsuranceName` | nvarchar(50) |  |  |  | N'人保' | 保司名称 |
| `cName` | nvarchar(50) |  |  |  |  | 承保机构名称 |
| `cCode` | varchar(50) |  |  |  |  | 承保机构编码 |
| `cCity` | nvarchar(50) |  |  |  |  | 省市区 |
| `province` | nvarchar(50) |  |  |  |  | 省 |
| `city` | nvarchar(50) |  |  |  |  | 城市 |
| `district` | nvarchar(50) |  |  |  |  | 地区 |
| `tCreateDate` | datetime |  |  |  | getdate() |  |
| `cAddress` | nvarchar(200) |  |  |  |  | 地址 |
| `cNo` | varchar(50) |  |  |  |  | 社会统一信用代码 |
| `cNoticePhone` | varchar(150) |  |  |  |  | 通知人手机号 |

## T_PProduct_GuaranteeInsDetail

*订单保险明细*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(200) |  |  |  |  | 保险明细名称 |
| `fProjectId` | int |  |  |  |  | 项目表id |
| `fGuaranteeId` | int |  |  |  |  | 订单id |
| `cNewGuid` | varchar(50) |  |  |  |  | 订单号 |
| `fItemID` | int |  |  |  |  | 分类ID 管理T_PProduct_InsItemInfo |
| `cItemName` | nvarchar(200) |  |  |  |  | 分类名称 |
| `fItemSort` | int |  |  |  |  | 保险信息分类排序 |
| `fAmount` | decimal(18,2) |  |  |  |  | 保额（区间限制时为默认值） |
| `cUnit` | nvarchar(200) |  |  |  |  | 计量单位 |
| `fPremium` | decimal(18,2) |  |  |  |  | 保费 |
| `fType` | tinyint |  |  |  |  | 1固定 2自定义 |
| `fSort` | int |  |  |  |  | 排序 |
| `fInsDetailInfoId` | int |  |  |  |  | 保险信息明细信息表id |
| `tCreateTime` | datetime |  |  |  |  |  |

## T_Enterprise_Mac

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cMac` | varchar(50) |  |  | 否 |  | mac地址 |
| `cEnterpriseNameCode` | varchar(50) |  |  |  |  | 统一社会编码 |
| `cRealName` | nvarchar(50) |  |  |  |  | 联系人 |
| `fState` | tinyint |  |  | 否 | 0 | 0：未使用，1：已使用 |
| `tdate` | datetime |  |  | 否 | getdate() | 添加时间 |
| `subdate` | datetime |  |  |  |  | 使用时间 |

## T_PProduct_SXPushIndex

*推送次数记录表，生成工资保证金账户收支编号用到*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `tDate` | date |  |  | 否 |  |  |
| `fIndex` | int |  |  | 否 |  |  |
| `fType` | tinyint |  |  | 否 | 1 | 1：纯线下工资监管，2：在线投保（太原） |

## T_Guarantee_AuditLog

*人工审核保单日志*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  |  | (0) | 保单表ID |
| `fPaylogID` | int |  |  |  | 0 | 支付记录表ID |
| `cAuditMessage` | nvarchar(50) |  |  |  |  | 审核备注说明 |
| `cAuditUserName` | nvarchar(20) |  |  |  |  | 审核人 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |

## T_GzZrx_InvoiceLog

*雇主责任险--发票申请记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cUserID` | varchar(50) |  |  |  |  | 用户ID，关联T_GzZrx_Users表ID |
| `fEnterpriseInfoID` | int |  |  |  | 0 | 企业表ID |
| `fType` | tinyint |  |  |  |  | 0普票电子发票，1普票纸质发票，2专票纸质发票 |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 企业名称 |
| `cEnterpriseNameCode` | varchar(50) |  |  |  |  | 统一社会信用代码 |
| `cUser` | nvarchar(20) |  |  |  |  | 联系人 |
| `cUserPhone` | varchar(50) |  |  |  |  | 联系人手机 |
| `cAddress` | nvarchar(50) |  |  |  |  | 发票邮寄地址 |
| `cEmail` | nvarchar(40) |  |  |  |  | 电子邮箱 |
| `cBank` | nvarchar(30) |  |  |  |  | 开户行 |
| `cAccount` | nvarchar(30) |  |  |  |  | 开户账号 |
| `fGuaranteeInfoID` | int |  |  |  | 0 | 保单表ID |
| `fInvoiceAmount` | numeric(18,2) |  |  |  | 0 | 发票金额 |
| `fState` | tinyint |  |  |  |  | 状态：0申请(用户向我方申请开票)，1 提交中(向保险公司申请开票) 2提交(保险公司开票成功)，3已推送(开票后向中心接口推送)，4推送失败(开票后向中心接口推送)，9自动生成一条 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |
| `tAppTime` | datetime |  |  |  |  | 用户申请时间 |
| `tSubTime` | datetime |  |  |  |  | 开票时间 |
| `invoiceUrl` | varchar(300) |  |  |  |  | 电子发票下载地址 |
| `invoiceLocalUrl` | varchar(200) |  |  |  |  | 电子发票OSS下载地址 |
| `invoiceCode` | varchar(50) |  |  |  |  | 发票代码 |
| `invoiceNo` | varchar(50) |  |  |  |  | 发票号码 |
| `ErrMsg` | nvarchar(200) |  |  |  |  | 在线开票失败原因 |
| `platformCode` | varchar(50) |  |  |  |  |  |
| `cTel` | varchar(20) |  |  |  |  | 税务登记联系电话 |
| `cCompanyAddress` | nvarchar(100) |  |  |  |  | 税务登记地址 |
| `cRemarks` | nvarchar(100) |  |  |  |  | 备注 |
| `fSendEmail` | tinyint |  |  | 否 | 0 |  |
| `emailId` | int |  |  | 否 | 0 |  |
| `fInsuranceType` | tinyint |  |  | 否 | 0 | 险种类型 0 雇主责任险 1 货运险 |

## T_GzZrx_InsuranceInfo

*雇主责任险-金融机构表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cInsuranceCode` | varchar(20) |  |  | 否 |  | 金融机构编码 |
| `cInsuranceName` | nvarchar(20) |  |  | 否 |  | 金融机构名称 |
| `cInsuranceFullName` | nvarchar(50) |  |  |  |  | 金融机构全称 |
| `fInsuranceType` | tinyint |  |  | 否 | 0 | 金融机构类型 0 保险公司 1 银行 2 担保公司 |
| `cInsuranceLogo` | varchar(100) |  |  |  |  | 金融机构logo |
| `cOrderLogo` | varchar(100) |  |  |  |  | 订单logo |
| `cInvoiceTitle` | nvarchar(100) |  |  |  |  | 发票申请窗口名称 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |

## T_Enterprise_BlackLog

*黑名单拦截记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fGuaranteeID` | int |  |  |  | 0 | 关联T_Guarantee_Info表ID |
| `fBlackPRCID` | int |  |  |  | 0 |  |
| `fDisableType` | tinyint |  |  |  | 0 | 冗余字段，禁用类型，默认0永久，1短期 |
| `tEndTime` | datetime |  |  |  |  | 冗余字段，禁用止期 |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `cInsuranceCompany` | varchar(50) |  |  |  |  | 冗余字段，承保机构 |
| `platformcode` | varchar(50) |  |  |  |  | 冗余字段，平台码 |

## T_zijin_interface

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `Prc_id` | int |  |  |  |  | T_PRC_Info表id |
| `CdUrl` | varchar(200) |  |  |  |  | 出单接口地址 |
| `PdUrl` | varchar(200) |  |  |  |  | 批单接口 |
| `FpUrl` | varchar(200) |  |  |  |  | 发票接口请求地址 |
| `TbUrl` | varchar(200) |  |  |  |  | 退保接口地址 |

## T_PProductYz_Coinsurant

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCID` | nvarchar(MAX) |  |  |  |  | 渠道ID 关联T_PProductYz_RPC |
| `cCoinsurantCode` | nvarchar(50) |  |  |  |  | 共保体编码 |
| `cUser` | nvarchar(50) |  |  |  |  | 联系人 |
| `cPhone` | nvarchar(50) |  |  |  |  | 联系人电话 |
| `fPrincipalID` | int |  |  |  |  | 主共ID 关联T_Insurance_Info |
| `cSecondaryID` | nvarchar(MAX) |  |  |  |  | 从共ID 拼接，隔开 |
| `cPrincipalUserPhone` | nvarchar(MAX) |  |  |  |  | 主共联系人 拼接，隔开 |
| `cSecondaryUserPhone` | nvarchar(MAX) |  |  |  |  | 从共联系人 拼接，隔开 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cName` | nvarchar(50) |  |  |  |  |  |
| `cCode` | nvarchar(50) |  |  |  |  | 共保体编码 |
| `fState` | tinyint |  |  |  |  |  |
| `cSecondaryName` | nvarchar(MAX) |  |  |  |  |  |
| `cPrincipalName` | nvarchar(50) |  |  |  |  |  |
| `cPRCName` | nvarchar(MAX) |  |  |  |  |  |
| `cRemark` | nvarchar(MAX) |  |  |  |  |  |

## T_PProduct_GuaranteeLaborUnit

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cLaborName` | nvarchar(255) |  |  |  |  | 劳务单位名称 |
| `cLaborCode` | nvarchar(255) |  |  |  |  | 劳务单位编码 |
| `cContactName` | nvarchar(255) |  |  |  |  | 联系人姓名 |
| `cContactPhone` | nvarchar(255) |  |  |  |  | 联系人电话 |
| `cNewGuid` | varchar(50) |  |  | 否 |  | cNewGuid（外键关联保单表Guarantee） |

## T_Guarantee_Cancel

*保单申请撤销表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cPolicyNo` | varchar(50) | 是 |  | 否 |  | 保单号 |
| `cApply_no` | varchar(50) |  |  |  |  | 业务申请码 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |
| `fResult` | tinyint |  |  |  |  | 0：审核中，1：审核通过，2：审核不通过 |
| `accept_no` | varchar(50) |  |  |  |  | 受理流水号 |
| `cError` | nvarchar(150) |  |  |  |  | 失败原因 |

## T_ZX_PointsUser

*担保小程序-积分用户表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fZXUserID` | int |  |  |  | 0 | 关联T_ZX_User表ID |
| `fTotal` | int |  |  |  | 0 | 总计 |
| `fUsed` | int |  |  |  | 0 | 已经用过统计 |
| `fLeft` | int |  |  |  | 0 | 剩余可用统计 |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |

## VerificationCode

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `Code` | nvarchar(50) |  |  |  |  |  |
| `token` | nvarchar(50) |  |  |  |  |  |
| `code_errornum` | int |  |  |  | 0 |  |
| `DataState` | int |  |  |  | 0 |  |
| `isCheck` | nvarchar(50) |  |  |  |  |  |
| `JoinDate` | datetime |  |  |  | getdate() |  |

## T_NJDT_PrcChannel

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fPrcRelationId` | int |  |  |  |  |  |
| `fChannelId` | int |  |  |  |  |  |

## T_ZX_GuaranteeBatch

*振鑫小程序-投标批次表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fZXUserID` | int |  |  |  |  | 关联T_ZX_User表ID |
| `cBatchNum` | varchar(50) |  |  |  |  | 批次号，用于前端传值、 |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 投保企业:若存在多家，则展示一家企业名称+....等多家 |
| `cMainPlatformcode` | varchar(20) |  |  |  |  | 主平台码 |
| `platformcode` | varchar(20) |  |  |  |  | 平台码 |
| `cFullCity` | nvarchar(200) |  |  |  |  | 投标地区 |
| `cInsuranceCompany` | varchar(20) |  |  |  |  | 机构简称，比如人保 |
| `instname` | varchar(50) |  |  |  |  | 承保机构全称，比如：中国人民财产保险股份有限公司舟山市分公司 |
| `cPolicyTmpID` | int |  |  |  |  | 模板记录ID 即T_Insurance_File表ID |
| `cPolicyTmp` | varchar(200) |  |  |  |  | 保函模板地址 |
| `cOwnerUnit` | nvarchar(200) |  |  |  |  | 招标人 |
| `cOwnerUnitCode` | nvarchar(100) |  |  |  |  | 招标人代码 |
| `cProjectName` | nvarchar(200) |  |  |  |  | 项目名称 |
| `cProjectNo` | nvarchar(100) |  |  |  |  | 项目编号 |
| `cBidName` | nvarchar(200) |  |  |  |  | 标段名称 |
| `cBidId` | nvarchar(100) |  |  |  |  | 标段编号 |
| `fMarginAmount` | decimal(18,2) |  |  |  | 0 | 保证金金额 |
| `fBidTime` | datetime |  |  |  |  | 开标时间 |
| `tGuaranteeStartTime` | datetime |  |  |  |  | 担保起期 |
| `tGuaranteeEndTime` | datetime |  |  |  |  | 担保止期 |
| `fGuaranteeDay` | int |  |  |  | 0 | 担保天数 |
| `fSinglePremium` | decimal(18,2) |  |  |  | 0 | 单笔保费（原价） |
| `fMarkPremium` | decimal(18,2) |  |  |  | 0 | 单笔保费（标价） |
| `fSFPremium` | decimal(18,2) |  |  |  | 0 | 总实收金额（总支付金额） |
| `fYHPremium` | decimal(18,2) |  |  |  | 0 | 优惠总金额 |
| `fState` | tinyint |  |  |  | 99 | 状态：14已关闭，6已出函，4已支付出函中，2待支付，0待预览确认，98企业待选择，99投保信息待补充，101 部分退保，1：已退保 |
| `fGuaranteeCount` | int |  |  |  | 0 | 批次关联的订单个数 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `fExtendDays` | int |  |  |  | 0 | 延长天数 ，当类型为用户输入时才>0 |
| `cPaymentSerialNumber` | varchar(10) |  |  |  |  | 打款序列号 |
| `cPaymentVoucher` | varchar(100) |  |  |  |  | 打款凭证 |
| `fPayType` | tinyint |  |  | 否 | 0 | 默认0未选择支付方式  1 在线支付 2 对公支付 |
| `skAccount` | varchar(50) |  |  |  |  | 收款账号 |
| `fPayId` | int |  |  |  |  |  |
| `ErrorInfor` | nvarchar(50) |  |  |  |  |  |
| `fPay_Type` | tinyint |  |  |  |  | 支付方式 同承保关系表T_Relation_PRCEnInsurance：2对公，9微信，7对公/微信 |
| `fPRCEnInsuranceID` | int |  |  |  |  | 承保关系表T_Relation_PRCEnInsurance的ID |

## T_GzZrx_PRC

*二级渠道表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fChannelID` | int |  |  | 否 | 0 | 一级渠道ID |
| `cPrcCode` | varchar(50) |  |  | 否 |  | 二级渠道编码 |
| `cPrcName` | nvarchar(50) |  |  | 否 |  | 二级渠道名称 |
| `cPrcShortName` | nvarchar(20) |  |  |  |  | 二级渠道简称 |
| `cCity` | nvarchar(30) |  |  |  |  | 业务范围 省/市/区 |
| `cSheng` | nvarchar(20) |  |  |  |  | 省 |
| `cShi` | nvarchar(20) |  |  |  |  | 市 |
| `cQu` | nvarchar(20) |  |  |  |  | 区 |
| `fState` | tinyint |  |  | 否 | 0 | 状态 0 禁用 1 启用 |
| `cPlatformName` | nvarchar(50) |  |  |  |  | 平台名称 |
| `cPlatformRemark` | nvarchar(100) |  |  |  |  | 平台介绍 |
| `cLogo` | varchar(200) |  |  |  |  | 平台Logo |
| `cWebDomain` | varchar(100) |  |  |  |  | 网站域名 |
| `cPreFormalUrl` | varchar(100) |  |  |  |  | 网站域名不带http |
| `cAgencyRoleId` | varchar(50) |  |  |  |  | 代理类角色权限 |
| `cEnterpriseRoleId` | varchar(50) |  |  |  |  | 投保企业角色权限 |
| `cServiceId` | varchar(100) |  |  |  |  | 客服ID |
| `cServiceUrl` | varchar(100) |  |  |  |  | 客服链接 |
| `cServiceQQ` | varchar(20) |  |  |  |  | 客服QQ号 |
| `cServiceTel` | varchar(20) |  |  |  |  | 客服电话 |
| `cTechSupport` | nvarchar(100) |  |  |  |  | 网站底栏配置 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |

## T_GzZrx_BaseFile

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cNumber` | varchar(50) |  |  | 否 |  |  |
| `cName` | nvarchar(50) |  |  |  |  |  |
| `fType` | tinyint |  |  | 否 | 0 |  |
| `fFileType` | tinyint |  |  | 否 | 0 |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_PProductYz_CoinsurantLink

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fCoinsurantID` | int |  |  |  |  | T_PProductYz_Coinsurant ID |
| `fLinkID` | int |  |  |  |  | 关联表ID   （根据 fType： 1渠道，对应T_PProductYz_PRC； 2主共 3从共 对应  T_PProduct_InsuranceInfo ） |
| `cName` | nvarchar(50) |  |  |  |  | 联系人 |
| `cPhone` | nvarchar(50) |  |  |  |  | 联系电话 |
| `cCustomerServicePhone` | nvarchar(50) |  |  |  |  | 客服电话 |
| `fType` | int |  |  |  |  | 类型 1渠道 2主共 3从共 |
| `tCreateTime` | datetime |  |  |  |  |  |

## T_PProduct_GuaranteeProjectPayList

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  | 否 |  |  |
| `cStepName` | nvarchar(50) |  |  | 否 |  |  |
| `tStepDate` | datetime |  |  | 否 |  |  |
| `fAmount` | decimal(18,2) |  |  | 否 |  |  |

## T_PProduct_InsuranceInfo

*多险种保险公司表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cInsuranceName` | nvarchar(50) |  |  | 否 |  | 机构简称 |
| `cInsuranceFullName` | nvarchar(50) |  |  |  |  | 机构全称 |
| `cOrderLogo` | varchar(200) |  |  |  |  | 订单logo |
| `cInsuranceLogo` | varchar(200) |  |  |  |  | 保险logo |
| `tdate` | datetime |  |  | 否 | getdate() | 创建时间 |
| `cInvoiceTitle` | nvarchar(200) |  |  |  |  |  |
| `fInsuranceType` | tinyint |  |  |  | 0 |  |
| `fInsuranceCode` | nvarchar(50) |  |  |  |  |  |

## T_NJDT_PRCShowInfo

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cCode` | varchar(50) |  |  |  |  | 模板编码 |
| `cDisplayName` | nvarchar(50) |  |  |  |  | 显示名称 |
| `fIsShow` | tinyint |  |  |  | 1 | 是否显示（0：否；1：是) |
| `fIsMust` | tinyint |  |  |  | 0 | 是否必填（0：否；1：是) |
| `fShowInfoId` | int |  |  |  |  | T_NJDT_ShowInfoTemplate 表id |
| `fPrcId` | int |  |  |  |  |  |

## T_ChannelOrder_ChannelInfo

*渠道信息*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(50) |  |  |  |  | 渠道名称 |
| `cContactName` | nvarchar(50) |  |  |  |  | 渠道委托联系人 |
| `cContactTel` | varchar(20) |  |  |  |  | 业务预留电话 |
| `fState` | tinyint |  |  |  |  | 状态 0：禁用；1：启用 |
| `cCodeDesc` | nvarchar(500) |  |  |  |  | 渠道码范围描述 |
| `cDesc` | nvarchar(500) |  |  |  |  | 渠道其他备注 |
| `tCreateTime` | datetime |  |  |  | getdate() |  |

## T_PProductYz_Enclosure

*医责险-附件模板类型*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cEnclosureName` | varchar(200) |  |  |  |  |  |
| `cEnclosureCode` | varchar(50) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cLastEditUser` | nvarchar(50) |  |  |  |  | 最后修改人 |
| `tLastEditTime` | datetime |  |  |  |  | 最后修改时间 |
| `fFlieType` | tinyint |  |  |  |  | 文件类型 1图片 2文件 3压缩包 |

## T_PProduct_GuaranteeService

*农民工延时赔付*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fProjectID` | int |  |  |  | 0 | 项目表ID |
| `fGuaranteeID` | int |  |  |  | 0 | 保单表ID |
| `cRemarks` | nvarchar(300) |  |  |  |  | 发起赔付、延期备注说明 |
| `fType` | tinyint |  |  |  | 0 | 类型，0延期，1赔付 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |
| `fPayMentState` | tinyint |  |  |  | 0 | 赔付状态，0无，1等待处理，2已受理，3拒绝受理，9已赔付 |
| `tLastPayMentTime` | datetime |  |  |  |  | 最近一次赔付状态时间 |
| `cPaymentRemarks` | nvarchar(300) |  |  |  |  | 延期受理备注 |
| `tPayMentTime` | datetime |  |  |  |  | 延期受理时间 |
| `cReject` | nvarchar(300) |  |  |  |  | 赔付拒绝原因 |
| `fParentID` | int |  |  |  | 0 | 赔付发起的对应ID |
| `cNewGuid` | varchar(50) |  |  |  |  | 唯一性标识 |
| `fDelayState` | tinyint |  |  |  | 0 | 延期状态，0无，1待办理延期，2延期已受理（已延期），6无需延期 |
| `tLastDelayTime` | datetime |  |  |  |  | 延期至时间 |
| `cPaymentVoucher` | varchar(100) |  |  |  |  | 延期保证金缴纳凭证 |
| `cDelayRemarks` | nvarchar(300) |  |  |  |  | 延期受理备注 |
| `tDelayTime` | datetime |  |  |  |  |  |
| `fIsBusinessTypeChanged` | tinyint |  |  |  | 0 | 是否缴纳方式有变更，默认0无，1有 |
| `fIsDelayShow` | tinyint |  |  |  | 1 | 是否延期显示，0不显示，默认1显示 |
| `cUserID` | varchar(50) |  |  |  |  | 录入的用户ID，对应T_PProduct_Admin表ID |
| `cUserName` | nvarchar(50) |  |  |  |  | 录入的用户ID名称 |

## T_Guarantee_DataBak

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `fGuaranteeInfoID` | int |  |  |  | 0 | T_Guarantee_Info表ID |
| `cPGPolicyUrl` | varchar(500) |  |  |  |  | 批单后的下载地址 |
| `cPGPolicyLocalUrl` | varchar(500) |  |  |  |  | 批单后的本地下载地址 |
| `CreateTime` | datetime |  |  |  | getdate() | 创建时间 |

## T_Epoint_PushGuaranteeLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `GuaranteeId` | int |  |  |  |  | T_Epoint_PushGuarantee表ID |
| `Operator` | nvarchar(50) |  |  |  |  | 操作人 |
| `OperationTime` | datetime |  |  |  |  | 操作时间 |
| `OperationType` | nvarchar(50) |  |  |  |  | 操作类型 |
| `OperationLog` | nvarchar(MAX) |  |  |  |  | 历史数据（操作记录） |
| `ImportId` | int |  |  |  |  | 导入记录表ID |

## T_Base_Area_ZY_cw

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cCode` | varchar(10) |  |  | 否 |  |  |
| `cParentCode` | varchar(10) |  |  |  |  |  |
| `cName` | nvarchar(50) |  |  | 否 |  |  |
| `fLevel` | int |  |  |  |  |  |

## T_Guarantee_Info_yx

*投保单信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  | 否 |  |  |
| `cEnterpriseName` | nvarchar(200) |  |  |  |  | 企业名称 |
| `cEnterpriseNameCode` | nvarchar(100) |  |  |  |  | 统一社会信用代码 |
| `cCorporationName` | nvarchar(20) |  |  |  |  | 法人姓名 |
| `cBank` | nvarchar(50) |  |  |  |  | 基本户开户行 |
| `cBankCardNo` | varchar(50) |  |  |  |  | 基本户账号 |
| `fUserID` | int |  |  |  | 0 |  |
| `cRealName` | nvarchar(50) |  |  |  |  | 联系人姓名 |
| `cPhone` | nvarchar(100) |  |  |  |  | 联系人手机号码 |
| `cEmail` | varchar(50) |  |  |  |  | 联系人邮箱 |
| `cAddress` | nvarchar(100) |  |  |  |  | 联系人地址 |
| `fProjectID` | int |  |  |  |  | 项目信息表自增ID |
| `cToEsignUrl` | nvarchar(200) |  |  |  |  | 待签章文件地址 |
| `cEsignUrl` | nvarchar(200) |  |  |  |  | 投保单签章文件地址 |
| `tEsignTime` | datetime |  |  |  |  | 签章时间 |
| `fRate` | decimal(10,3) |  |  |  | 0 | 费率（%） |
| `fPremium` | decimal(18,2) |  |  |  | 0 | 保费(元) |
| `cPolicyNo` | nvarchar(50) |  |  |  |  | 人保保单号 |
| `cPolicyUrl` | varchar(500) |  |  |  |  | 人保保单下载地址 |
| `cPolicyLocalUrl` | varchar(500) |  |  |  |  | 人保保单本地地址 |
| `tReceivePolicyTime` | datetime |  |  |  |  | 人保保单接收时间 |
| `tPolicyTime` | datetime |  |  |  |  | 人保保单生成时间 |
| `fState` | tinyint |  |  |  | 0 | 状态（0默认未签章，2已签章，3付款未到账，4已付款，5付款异常，6已出函，10已出具发票 |
| `tGuaranteedTime` | datetime |  |  |  |  | 出函时间 |
| `cPaymentSerialNumber` | nvarchar(50) |  |  |  |  | 打款序列号 |
| `cPaymentVoucher` | nvarchar(100) |  |  |  |  | 付款凭证上传地址 |
| `tPaymentVoucherTime` | datetime |  |  |  |  | 付款凭证上传时间 |
| `CreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `UUID` | nvarchar(150) |  |  |  |  | 人保影像传递用 投保时生产uuid,影像接口需要再次用到 |
| `cPolicyZipUrl` | nvarchar(500) |  |  |  |  | 提供给人保下载的zip文件路径 |
| `cPolicyZipName` | nvarchar(100) |  |  |  |  | 提供给人保下载的zip文件名 |
| `cInsuranceCompany` | nvarchar(50) |  |  |  |  | 保险公司名称 |
| `tEffectiveTime` | datetime |  |  |  |  | 有效保函有效时间 |
| `fIsPush` | tinyint |  |  |  | 0 | 是否已经推送，默认0未推送，1推送成功,2:已推送加密保函，3保函已解密 |
| `tPushTime` | datetime |  |  |  |  | 推送时间 |
| `tPushSuccessTime` | datetime |  |  |  |  | 成功推送记录时间 |
| `cPayBank` | nvarchar(50) |  |  |  |  | 保费支付银行 |
| `cPayBankCardNo` | varchar(50) |  |  |  |  | 保费支付银行账号 |
| `tPayTime` | datetime |  |  |  |  | 保费支付时间 |
| `fAuditType` | tinyint |  |  |  |  | 0：自动审核，1：人工审核 |
| `tAuditTime` | datetime |  |  |  |  | 审核时间 |
| `cMac` | varchar(50) |  |  |  |  | 投标电脑MAC地址 |
| `cHardDisk` | varchar(50) |  |  |  |  | 投标电脑硬盘序列号 |
| `cCPU` | varchar(50) |  |  |  |  | 投标电脑CPU序列号 |
| `cIP` | varchar(50) |  |  |  |  | 投标电脑公网IP |
| `fPayId` | int |  |  |  |  |  |
| `cAuditMessage` | nvarchar(50) |  |  |  |  | 人工审核备注 |
| `cNewGuid` | varchar(50) |  |  | 否 |  | 唯一性标识 |
| `PolicyUpdateTime` | datetime |  |  |  |  | 保函文件下载时间 |
| `ErrorInfor` | nvarchar(200) |  |  |  |  | 异常信息 |
| `fzipIsPush` | tinyint |  |  | 否 |  | 推送ZIP文件，0：未打包，1：已打包，2：已推送 |
| `platformcode` | varchar(50) |  |  |  |  | 平台编码 |
| `cBidId_encryption` | varchar(500) |  |  |  |  | 标段编号密文 |
| `cBidName_encryption` | varchar(1000) |  |  |  |  | 标段名称密文 |
| `cOwnerUnit_encryption` | varchar(500) |  |  |  |  | 招标人密文 |
| `cOwnerUnitCode_encryption` | varchar(500) |  |  |  |  | 招标人统一社会编码密文 |
| `DecryptionKey` | varchar(50) |  |  |  |  | 解密密钥 |
| `fMarginAmount` | decimal(18,2) |  |  | 否 | 0 | 保证金金额 |
| `EndorseNo` | varchar(50) |  |  |  |  | 批单号 |
| `cPGPolicyUrl` | varchar(500) |  |  |  |  | 批单后的下载地址 |
| `cPGPolicyLocalUrl` | varchar(500) |  |  |  |  | 批单后的本地下载地址 |
| `cPGUUID` | varchar(60) |  |  |  |  | 批单UUID |
| `tPGTime` | datetime |  |  |  |  | 批改时间 |
| `cInsuranceCode` | varchar(64) |  |  |  |  |  |
| `cProposalno` | nvarchar(100) |  |  |  |  |  |
| `cPayurl` | varchar(800) |  |  |  |  |  |
| `cCompanyTel` | varchar(50) |  |  |  |  |  |
| `cCompanyAddress` | nvarchar(100) |  |  |  |  |  |
| `cOrderId` | varchar(50) |  |  |  |  |  |
| `tOrderTime` | datetime |  |  |  |  |  |
| `cPolicyPzUrl` | varchar(500) |  |  |  |  | 保险凭证下载地址 |
| `fGProjectId` | int |  |  | 否 |  |  |
| `fInvoiceType` | tinyint |  |  |  |  |  |
| `cPGPolicyPzUrl` | varchar(500) |  |  |  |  |  |
| `pushEvidence` | tinyint |  |  | 否 |  | 是否推送e签宝存证 0 否 1是 |
| `claimsState` | tinyint |  |  | 否 |  |  |
| `quitIsPush` | tinyint |  |  | 否 |  |  |
| `AreaCode` | varchar(50) |  |  |  |  |  |
| `tQuitApplyTime` | datetime |  |  |  |  |  |
| `fQuitState` | tinyint |  |  | 否 | 0 |  |
| `fCouponID` | int |  |  | 否 | 0 |  |
| `cCouponDes` | nvarchar(50) |  |  |  |  |  |
| `cAuditUserName` | nvarchar(50) |  |  |  |  |  |
| `fPayType` | int |  |  | 否 | 0 |  |
| `skAccount` | varchar(50) |  |  |  |  |  |
| `bzjenddate_encryption` | varchar(200) |  |  |  |  |  |
| `insuredcontactname_encryption` | varchar(200) |  |  |  |  |  |
| `insuredcontactphone_encryption` | varchar(200) |  |  |  |  |  |
| `insuredaddress_encryption` | varchar(200) |  |  |  |  |  |
| `cAgency` | varchar(500) |  |  | 否 | '' |  |
| `cTenderer_address` | varchar(500) |  |  | 否 | '' |  |
| `cProjectNo_encryption` | varchar(500) |  |  | 否 | '' |  |
| `cProjectName_encryption` | varchar(1000) |  |  |  | '' |  |
| `cProjectArea_encryption` | varchar(500) |  |  | 否 | '' |  |
| `fFender_expire` | int |  |  | 否 | 0 |  |
| `cContactIDNo` | varchar(50) |  |  | 否 | '' |  |
| `cBidFileUrls` | varchar(1000) |  |  | 否 | '' |  |
| `tender_type` | nvarchar(30) |  |  | 否 | '' |  |
| `fCoInsuranceState` | tinyint |  |  | 否 | 0 |  |
| `CheckTime` | datetime |  |  |  |  |  |
| `third_UUID` | varchar(50) |  |  |  |  |  |
| `fMainCo` | tinyint |  |  | 否 | 0 |  |

## T_XK_RebateDetail

*返点申请明细*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fRebateInfoId` | int |  |  |  |  | T_XK_RebateInfo 表id |
| `fGuaranteeId` | int |  |  |  |  | 返点订单表id |
| `tCreateDate` | datetime |  |  |  | getdate() |  |
| `fRebateStatus` | tinyint |  |  |  | 1 | 返点状态（1：返点中；2：已返点） |
| `tRebateTime` | datetime |  |  |  |  | 标记返点时间 |
| `fReturnStatus` | tinyint |  |  |  | 0 | 标记已退状态（0：未标记；1：已标记） |
| `fReturnAuthStatus` | tinyint |  |  |  | 0 | 标记已退审核结果（0：待处理；1：审核通过；2：审核驳回） |
| `cDesc` | nvarchar(200) |  |  |  |  | 备注 |

## T_PProduct_GuaranteeServiceFiles

*农民工延时赔付凭证附件表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fProjectID` | int |  |  |  | 0 | 项目表ID |
| `fGuaranteeID` | int |  |  |  | 0 | 保单表ID |
| `fGuaranteeServiceID` | int |  |  |  | 0 | T_PProduct_GuaranteeService表ID |
| `cFiles` | varchar(200) |  |  |  |  | 附件、凭证 |
| `CreateTime` | datetime |  |  |  | getdate() | 创建时间 |

## T_ZX_PrizeRecord_Order

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cReqOrderNo` | varchar(50) |  |  |  |  | 请求第三方的订单号 |
| `cWorkId` | varchar(50) |  |  |  |  | 在第三方的流水号 |
| `cPackageInfo` | nvarchar(300) |  |  |  |  | 跳转微信支付收款页的package信息 |
| `tSuccessTime` | datetime |  |  |  |  | 成功领取时间 |
| `cErrorInfo` | nvarchar(500) |  |  |  |  | 错误信息 |
| `fPrizeId` | int |  |  |  |  | 中奖记录表id |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `cDesc` | nvarchar(200) |  |  |  |  | 备注 |

## T_NJDT_Menus

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `Code` | nvarchar(20) |  |  | 否 |  | 编码 |
| `CreateDateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `IsDeleted` | bit |  |  | 否 | 0 | 是否删除 |
| `Name` | nvarchar(20) |  |  | 否 |  | 菜单名称 |
| `Order` | int |  |  | 否 |  | 排序越大越靠后 |
| `PathCode` | nvarchar(50) |  |  | 否 |  | 路径码=(上级的路径码+当前的Code) |
| `Type` | tinyint |  |  | 否 |  | 菜单类型 |
| `Url` | nvarchar(300) |  |  | 否 |  |  |
| `Onclick` | nvarchar(20) |  |  |  |  | 按钮点击事件 |
| `ParentId` | int |  |  |  |  | 上级菜单ID |
| `Icon` | varchar(50) |  |  |  |  |  |

## T_GzZrx_InsuranceFileTemplateBase

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fInsuranceID` | int |  |  | 否 | 0 |  |
| `cName` | nvarchar(50) |  |  |  |  |  |
| `fIsDefault` | tinyint |  |  | 否 | 0 |  |
| `fInsuranceTypeID` | int |  |  | 否 | 0 |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_Guarantee_MonthData

*月份报表数据表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `tyear` | int |  |  |  | 0 | 年 |
| `tmonth` | int |  |  |  | 0 | 月 |
| `cFileUrl` | varchar(200) |  |  |  |  | 报表文件地址 |
| `CreateTime` | datetime |  |  |  | getdate() | 创建时间 |

## T_GzZrx_Menus

*雇主责任险-用户公共菜单表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Id` | varchar(50) | 是 |  | 否 |  |  |
| `Code` | nvarchar(6) |  |  | 否 |  |  |
| `CreateDateTime` | datetime |  |  | 否 |  |  |
| `IsDeleted` | bit |  |  | 否 |  |  |
| `Name` | nvarchar(20) |  |  | 否 |  |  |
| `Order` | int |  |  | 否 |  |  |
| `ParentId` | varchar(50) |  |  |  |  |  |
| `PathCode` | nvarchar(20) |  |  | 否 |  |  |
| `Type` | tinyint |  |  | 否 |  |  |
| `Url` | nvarchar(300) |  |  | 否 |  |  |
| `Icon` | varchar(150) |  |  |  |  | 图标 |
| `Onclick` | nvarchar(20) |  |  |  |  |  |
| `fTag` | tinyint |  |  |  | 0 | 默认0传化责任险 |
| `cAction` | varchar(50) |  |  |  |  | 接口 |

## T_XK_RebateBatchRelation

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fRebateBatchId` | int |  |  |  |  | 返点批次表id |
| `fRebateInfoId` | int |  |  |  |  | 返点申请表id |
| `fType` | tinyint |  |  |  |  | 关联类型（1：支付宝；2：银行卡；0：全部-1.4版本加入） |

## T_PProductYz_MedicalAccident

*医责险-事故信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cNo` | varchar(50) |  |  | 否 |  | 事故编号 |
| `fEnterpriseInfoID` | int |  |  | 否 | 0 | 投保人id |
| `cEnterpriseName` | nvarchar(50) |  |  | 否 |  | 投保人名称 |
| `fGuaranteeId` | int |  |  | 否 |  | 保单id |
| `cPolicyNo` | varchar(50) |  |  | 否 |  |  |
| `cDoctorName` | nvarchar(50) |  |  | 否 |  |  |
| `tDate` | date |  |  | 否 |  | 诊疗时间 |
| `cOffice` | nvarchar(50) |  |  | 否 |  | 医院科室 |
| `cPatientName` | nvarchar(50) |  |  | 否 |  | 患者姓名 |
| `fPatientSex` | tinyint |  |  | 否 |  | 患者性别（1：男；2：女） |
| `cPatientCardID` | varchar(50) |  |  | 否 |  | 患者身份证号 |
| `cPatientNation` | nvarchar(50) |  |  | 否 |  | 患者民族 |
| `cPatientAddress` | nvarchar(200) |  |  | 否 |  | 患者住址 |
| `cPatientPhone` | varchar(20) |  |  | 否 |  | 患者电话 |
| `cProxyName` | nvarchar(50) |  |  |  |  | 代理人患者姓名 |
| `fProxySex` | tinyint |  |  |  |  | 代理人性别（1：男；2：女） |
| `cProxyCardID` | varchar(50) |  |  |  |  | 代理人身份证号 |
| `cProxyNation` | nvarchar(50) |  |  |  |  | 代理人民族 |
| `cProxyAddress` | nvarchar(200) |  |  |  |  | 代理人住址 |
| `cProxyPhone` | varchar(20) |  |  |  |  | 代理人电话 |
| `cProxyType` | tinyint |  |  |  | 0 | 代理人类型（1：个人，2：代理机构） |
| `cProxyGroupName` | nvarchar(50) |  |  |  |  | 代理机构名称 |
| `cContent` | nvarchar(500) |  |  | 否 |  | 简要诊疗经过 |
| `cDesc` | nvarchar(500) |  |  | 否 |  | 简要疑似事故过错描述 |
| `tCreateDate` | datetime |  |  |  | getdate() |  |
| `cUserName` | nvarchar(50) |  |  | 否 |  | 创建人 |
| `fShowYTW` | tinyint |  |  | 否 | 1 | 是否展现给医调委（0：不展现；1：展现） |
| `fShowCG` | tinyint |  |  | 否 | 1 | 是否展现给从共（0：不展现；1：展现） |

## T_PProduct_GuaranteeServiceLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fProjectID` | int |  |  |  | 0 | 对应T_PProduct_ProductInfo表ID |
| `fGuaranteeID` | int |  |  |  | 0 | 对应T_PProduct_Guarantee表ID |
| `fGuaranteeServiceID` | int |  |  |  | 0 | 对应T_PProduct_GuaranteeService表ID |
| `fPayMentState` | tinyint |  |  |  | 0 | 赔付状态，0无，1等待处理，2已受理，3拒绝受理，9已赔付 |
| `cRemarks` | nvarchar(300) |  |  |  |  |  |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |
| `fType` | tinyint |  |  |  | 0 | 类型，0延期，1赔付 |
| `fDelayState` | tinyint |  |  |  | 0 | 延期状态，0无，1待办理延期，2延期已受理（已延期），6无需延期 |
| `tLastDelayTime` | datetime |  |  |  |  | 延期至时间 |
| `cFiles` | varchar(300) |  |  |  |  | 延期保证金缴纳凭证 |
| `cUserID` | varchar(50) |  |  |  |  | 录入的用户ID，对应T_PProduct_Admin表ID |
| `cUserName` | nvarchar(50) |  |  |  |  | 录入的用户ID名称 |

## T_XK_RebateInfoCode

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cCode` | varchar(20) |  |  | 否 |  |  |
| `fIndex` | int |  |  | 否 |  |  |
| `fType` | tinyint |  |  |  | 1 | 1：返点申请批次管理；2：返点打款批次管理 |
| `tCreateDate` | datetime |  |  |  | getdate() |  |

## T_ChannelOrder_OrderInfo

*订单*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fDataFrom` | tinyint |  |  |  | 0 | 数据来源，1投标业务；2：代收业务；3：纯经济业务 |
| `applyno` | nvarchar(50) |  |  |  |  | 订单编号 |
| `platformcode` | nvarchar(50) |  |  |  |  |  |
| `platformname` | nvarchar(50) |  |  |  |  |  |
| `cInsuranceCompany` | nvarchar(20) |  |  |  |  | 金融机构 |
| `cPolicyNo` | varchar(50) |  |  |  |  | 保单号 |
| `cYWGS` | nvarchar(50) |  |  |  |  | 业务归属：自然流量或渠道业务或未分配 |
| `cGSQD` | nvarchar(50) |  |  |  |  | 归属渠道 : 渠道名称+渠道码 |
| `cSourceCode` | nvarchar(50) |  |  |  |  | 备注（邀请码） |
| `cEnterpriseNameCode` | nvarchar(50) |  |  |  |  | 投保企业名称 |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 投保企业信用代码 |
| `fPremium` | decimal(18,2) |  |  |  | 0 | 保费 |
| `fState` | tinyint |  |  |  |  | 订单状态，1:未出单；2：已出单；3：退保；4：无效单；5：归档后退保 |
| `fRebateAmount` | decimal(18,2) |  |  |  |  | 返点金额：归档后发生的返点金额 |
| `cProjectName` | nvarchar(50) |  |  |  |  |  |
| `cProjectNo` | nvarchar(50) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  |  | 原始订单创建时间 |
| `tPayTime` | datetime |  |  |  |  |  |
| `tGuaranteedTime` | datetime |  |  |  |  | 出函时间 |
| `tReturnTime` | datetime |  |  |  |  | 申请时间（标记已退时间） |
| `fBidTime` | datetime |  |  |  |  | 开标时间 |
| `fGDState` | tinyint |  |  |  | 0 | 归档状态 0：未归档；1：已归档 |
| `tGDTime` | datetime |  |  |  |  |  |
| `cGDBatch` | nvarchar(50) |  |  |  |  | 归档批次 |

## T_ZX_PrizeCount

*振鑫-活动次数*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `fZXUserID` | int | 是 |  | 否 |  | 关联T_ZX_User表ID |
| `fTag` | int | 是 |  | 否 | 0 | 活动标签，值1：618 新人注册抽奖活动 |
| `fSumCount` | int |  |  |  | 0 | 总次数 |
| `fUsedCount` | int |  |  |  | 0 | 已使用次数 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |

## T_SysOperation_Log

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cTable` | varchar(50) |  |  | 否 |  |  |
| `fTableID` | int |  |  | 否 |  |  |
| `cUser` | nvarchar(50) |  |  |  |  |  |
| `cOperation` | nvarchar(50) |  |  |  |  |  |
| `cRemark` | nvarchar(1000) |  |  |  |  |  |
| `cFileUrls` | varchar(500) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  | getdate() |  |
| `platformcode` | varchar(50) |  |  |  |  |  |
| `Prc_Type` | tinyint |  |  |  | 0 |  |
| `fBid` | int |  |  |  | 0 |  |
| `fType` | tinyint |  |  |  | 0 |  |

## T_XK_DictType

*线客字典类型表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `cTypeCode` | varchar(20) | 是 |  | 否 |  | 字典类型编码 |
| `cTypeName` | nvarchar(20) |  |  | 否 |  | 字典类型名称 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_PProductYz_Menus

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Id` | int | 是 | 是 | 否 |  |  |
| `Code` | nvarchar(20) |  |  | 否 |  | 编码 |
| `CreateDateTime` | datetime2 |  |  | 否 |  | 创建时间 |
| `IsDeleted` | bit |  |  | 否 |  | 是否删除 |
| `Name` | nvarchar(20) |  |  | 否 |  | 菜单名称 |
| `Order` | int |  |  | 否 |  | 排序越大越靠后 |
| `PathCode` | nvarchar(50) |  |  | 否 |  | 路径码=(上级的路径码+当前的Code) |
| `Type` | tinyint |  |  | 否 |  | 菜单类型 |
| `Url` | nvarchar(300) |  |  | 否 |  |  |
| `Onclick` | nvarchar(20) |  |  |  |  | 按钮点击事件 |
| `ParentId` | int |  |  |  |  | 上级菜单ID |

## T_PProduct_InsDetailInfo

*保险信息明细信息*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(200) |  |  |  |  |  |
| `fProgrammeID` | int |  |  |  |  |  |
| `fItemID` | int |  |  |  |  |  |
| `cItemName` | nvarchar(200) |  |  |  |  |  |
| `fAmount` | decimal(18,2) |  |  |  |  | 保额（区间限制时为默认值） |
| `cUnit` | nvarchar(200) |  |  |  |  | 计量单位 |
| `fPremium` | decimal(18,2) |  |  |  |  | 保费 |
| `fMinAmount` | decimal(18,2) |  |  |  |  | 最小保额 |
| `fMaxAmount` | decimal(18,2) |  |  |  |  | 最大保额 |
| `fType` | tinyint |  |  |  |  | 1固定 2自定义 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cItemList` | nvarchar(MAX) |  |  |  |  |  |
| `fSort` | int |  |  |  |  |  |

## T_Enterprise_SendMoney

*企业打款认证记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  | 企业表ID 外键 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `fAmount` | int |  |  |  |  | 金额，单位：分 |
| `fUsage` | int |  |  |  |  | 是否使用（0：未使用；1：已使用） |
| `cBank` | nvarchar(50) |  |  |  |  | 开户行全称 |
| `cBankCardNo` | nvarchar(50) |  |  |  |  | 卡号 |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 企业名称 |
| `cEnterpriseNameCode` | varchar(50) |  |  |  |  | 统一社会信用代码 |
| `ciSeqno` | varchar(50) |  |  |  |  |  |
| `cRecCityName` | varchar(50) |  |  |  |  | 开户行所在城市 |
| `cContactUserTel` | varchar(11) |  |  |  |  |  |

## T_GzZrx_Guarantee

*雇主责任险--订单表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fMianID` | int |  |  | 否 |  |  |
| `fGuaranteeId` | int |  |  | 否 |  |  |
| `cName` | nvarchar(50) |  |  | 否 |  | 姓名 |
| `cCardID` | varchar(20) |  |  | 否 |  | 身份证号 |
| `fPackageOptionId` | int |  |  | 否 | 0 | 职业类别ID（废弃） |
| `tStartTime` | datetime |  |  | 否 |  | 生效时间 |
| `tEndTime` | datetime |  |  | 否 |  | 截止时间 |
| `fState` | tinyint |  |  |  |  | 状态（0：正常投保；1：批增；2：批减(替换)） |
| `fTBState` | tinyint |  |  |  | 0 | 投保状态（0：未投保；1：已投保；3：作废）保司回调更新状态 |
| `tCreateTime` | datetime |  |  |  | getdate() |  |
| `fIsDelete` | tinyint |  |  | 否 | 0 | 是否删除（0：未删除；1：已删除） |
| `cUser` | nvarchar(50) |  |  |  |  |  |
| `cModifyUser` | nvarchar(50) |  |  |  |  | 修改人 |
| `tLastModifyDate` | datetime |  |  |  |  | 最后修改时间 |
| `fSex` | tinyint |  |  | 否 | 0 | 性别（0：女；1：男） |
| `fAge` | int |  |  | 否 |  | 年龄 |
| `cWorkName` | nvarchar(50) |  |  | 否 |  | 职业别名 |
| `fPremium` | decimal(18,2) |  |  | 否 | 0 | 保费 |
| `fPGGuaranteeId` | int |  |  | 否 | 0 | 操作批减的批单id |
| `fReplacedId` | int |  |  | 否 | 0 | 替换当前记录的雇员记录id（新雇员对应的id） |
| `cPackageOptionCode` | nvarchar(50) |  |  |  |  | T_GzZrx_PackageOption 表 cOptionCode |
| `fOldId` | int |  |  | 否 | 0 | 追溯id。老的记录id |

## T_PProductYz_SetShowRecord

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fRelateID` | int |  |  | 否 |  | fType=1，填T_PProductYz_MedicalAccident表id；fType=2：填T_PProductYz_Cliam表id |
| `fType` | tinyint |  |  |  | 0 | 类型：（1：事故分发记录；2：理赔分发记录） |
| `cAccount` | nvarchar(50) |  |  |  |  | 账号 |
| `cName` | nvarchar(50) |  |  |  |  | 姓名 |
| `instname` | nvarchar(50) |  |  |  |  | 所属公司 |
| `message` | nvarchar(50) |  |  |  |  | 分发类型 |
| `tCreateDate` | datetime |  |  |  | getdate() |  |

## T_Base_Area_ZY_cxp

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `代码` | nvarchar(255) |  |  |  |  |  |
| `上级代码` | nvarchar(255) |  |  |  |  |  |
| `名称` | nvarchar(255) |  |  |  |  |  |
| `代码级别` | nvarchar(255) |  |  |  |  |  |

## T_Guarantee_Source

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  | 否 |  | 企业表id |
| `fGuaranteeID` | int |  |  | 否 |  | 保单id |
| `cSourceCode` | nvarchar(50) |  |  |  |  | 来源码 |

## T_ZX_ProductInfo

*标后产品表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cProductId` | varchar(50) |  |  | 否 |  | 产品id |
| `cProductName` | nvarchar(30) |  |  |  |  | 产品名称 |
| `fState` | tinyint |  |  | 否 | 0 | 状态 0禁用 1启用 |
| `fSort` | int |  |  | 否 | 0 | 排序 数值大靠前 |
| `cFeature` | nvarchar(50) |  |  |  |  | 产品特点 |
| `cIntro` | nvarchar(1000) |  |  |  |  | 产品简介 |
| `cProductPic` | varchar(200) |  |  |  |  | 产品图片 |
| `cDesc` | nvarchar(3000) |  |  |  |  | 产品描述 |
| `cRemark` | nvarchar(200) |  |  |  |  | 备注 |
| `fRate` | decimal(10,2) |  |  | 否 | 1 | 费率% |
| `fMinPremium` | decimal(10,2) |  |  | 否 | 0 | 最低保费 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |
| `fType` | tinyint |  |  | 否 | 0 | 显示平台 0振鑫 1京山 2湖南小散 |
| `fInsType` | tinyint |  |  | 否 | 0 | 险种 (京山类型0:投标履约 1:施工履约保函 2:农民工工资保函 3:工程款支付保函 4:工程质量保证保函 5:安全生产责任险) |

## T_NJDT_ChannelCode

*渠道编码生产规则记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cPreCode` | varchar(50) |  |  |  |  |  |
| `cCode` | varchar(50) |  |  |  |  |  |
| `fIndex` | int |  |  |  |  |  |

## T_PProductYz_Organ

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cOrganName` | nvarchar(50) |  |  |  |  | 机构名称 |
| `cOrganCode` | nvarchar(50) |  |  |  |  | 机构编码 |
| `cPlatformProvince` | nvarchar(50) |  |  |  |  | 所在省 |
| `cPlatformCity` | nvarchar(50) |  |  |  |  | 所在市 |
| `cPlatformCounty` | nvarchar(50) |  |  |  |  | 所在县 |
| `cPlatformProvinceCode` | nvarchar(50) |  |  |  |  | 所在省编码 |
| `cPlatformCityCode` | nvarchar(50) |  |  |  |  | 所在市编码 |
| `cPlatformCountyCode` | nvarchar(50) |  |  |  |  | 所在县编码 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cAddress` | nvarchar(200) |  |  |  |  | 地址 |
| `cUser` | nvarchar(50) |  |  |  |  | 联系人 |
| `cUserPhone` | nvarchar(50) |  |  |  |  | 联系人电话 |
| `cNoticePhone` | nvarchar(50) |  |  |  |  | 通知人电话 |
| `cCityFullName` | nvarchar(50) |  |  |  |  |  |
| `cCode` | nvarchar(50) |  |  |  |  |  |
| `cYTWNoticePhone` | nvarchar(200) |  |  |  |  | 医调委通知手机号 |

## T_PProduct_InsDetailSelectInfo

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cItemList` | nvarchar(MAX) |  |  |  |  |  |
| `cName` | nvarchar(200) |  |  |  |  |  |

## T_GzZrx_InsuranceFileTemplate

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fInsuranceID` | int |  |  | 否 | 0 |  |
| `cName` | nvarchar(50) |  |  |  |  |  |
| `fIsDefault` | tinyint |  |  | 否 | 0 |  |
| `fInsuranceTypeID` | int |  |  | 否 | 0 |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_GzZrx_OperationLog

*雇主货运险-操作日志表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cTable` | varchar(50) |  |  | 否 |  | 业务表名 |
| `uuid` | varchar(50) |  |  | 否 |  | 业务表ID |
| `cUserID` | varchar(50) |  |  |  |  |  |
| `cUser` | nvarchar(20) |  |  |  |  | 操作人 |
| `cOperation` | nvarchar(50) |  |  |  |  | 标题 |
| `cRemark` | nvarchar(1000) |  |  |  |  | 内容 |
| `tCreateTime` | datetime |  |  |  | getdate() |  |
| `fFromTag` | tinyint |  |  |  | 0 | 0：PC端，1：H5端 |

## T_ZX_GoodsInfo

*振鑫小程序-商品信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fTypeID` | int |  |  |  | 0 | 商品类别，关联T_ZX_GoodsType商品类别表ID |
| `fNatureType` | int |  |  |  | 0 | 商品性质，默认0：卡券/兑换商品；1：实物/线下商品 |
| `cNum` | varchar(50) |  |  |  |  | 商品编号 |
| `cGoodsName` | nvarchar(50) |  |  |  |  | 商品名称 |
| `cGoodsPic` | varchar(200) |  |  |  |  | 商品列表图片地址，一张 |
| `cGoodsDes` | nvarchar(300) |  |  |  |  | 商品简单描述 |
| `cDescription` | nvarchar(2000) |  |  |  |  | 商品详情描述 |
| `fPrice` | decimal(10,2) |  |  |  | 0 | 市场价格 |
| `fPoints` | int |  |  |  | 0 | 商品单价所需积分 |
| `tUpTime` | datetime |  |  |  |  | 上架时间 |
| `tDownTime` | datetime |  |  |  |  | 下架时间 |
| `fState` | tinyint |  |  |  | 0 | 商品状态，默认0未上架，1已上架 |
| `fIsRecommend` | tinyint |  |  |  | 0 | 是否推荐，默认0否，1是 |
| `fInventoryCount` | int |  |  |  | 0 | 库存 |
| `fSalesCount` | int |  |  |  | 0 | 销量 |
| `fQuotaCount` | int |  |  |  | 0 | 限购数量 |
| `cMainPlatformcode` | varchar(20) |  |  |  |  | 客户端应用，主平台码 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `cAuditUserName` | nvarchar(20) |  |  |  |  | 后台添加审核人 |
| `cNewGuid` | varchar(50) |  |  |  |  | 唯一值，用于前端传值 |

## T_Guarantee_Surrender

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  | 0 |  |
| `fGuaranteeInfoID` | int |  |  |  | 0 |  |
| `CreateTime` | datetime |  |  |  |  |  |
| `fState` | tinyint |  |  |  | 0 | 0默认申请 |
| `cFileUrl` | varchar(250) |  |  |  |  | 申请书 |
| `tGetFileTime` | datetime |  |  |  |  | 下载时间 |
| `fType` | tinyint |  |  | 否 | 0 |  |

## T_NJDT_Channel

*渠道信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cPreCode` | varchar(50) |  |  |  |  |  |
| `cCode` | varchar(50) |  |  |  |  |  |
| `fIndex` | int |  |  |  |  |  |

## T_PProduct_EnterpriseSendMoney

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  |  |  |
| `fAmount` | int |  |  |  |  | 金额，单位：分 |
| `fUsage` | int |  |  |  |  | 是否使用（0：未使用；1：已使用） |
| `cBank` | nvarchar(50) |  |  |  |  | 开户行全称 |
| `cBankCardNo` | nvarchar(50) |  |  |  |  | 卡号 |
| `ciSeqno` | varchar(50) |  |  |  |  |  |
| `cRecCityName` | varchar(50) |  |  |  |  |  |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  |  |
| `cEnterpriseNameCode` | varchar(50) |  |  |  |  |  |
| `cContactUserTel` | varchar(11) |  |  |  |  |  |

## T_ZX_PointsType

*担保小程序-积分类型表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(30) |  |  |  |  | 积分名称 |
| `cDes` | nvarchar(50) |  |  |  |  | 描述 |
| `fPoints` | int |  |  |  | 0 | 积分 |
| `fCount` | int |  |  |  | 0 | 可获得次数 |
| `cEvent` | varchar(30) |  |  |  |  | 事件，由事件触发来发放积分 |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |

## T_PProduct_InsItemInfo

*保险信息分类信息*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(200) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  |  |  |
| `fSort` | int |  |  |  |  |  |

## T_Base_Area_ZY

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cCode` | varchar(10) |  |  | 否 |  |  |
| `cParentCode` | varchar(10) |  |  |  |  |  |
| `cName` | nvarchar(50) |  |  | 否 |  |  |
| `fLevel` | int |  |  |  |  |  |

## K_ToolUser

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `Account` | varchar(50) |  |  | 否 |  |  |
| `Password` | varchar(50) |  |  |  |  |  |
| `LastLoginTime` | datetime |  |  |  |  |  |
| `AuthCode` | varchar(50) |  |  |  |  |  |

## T_ZX_PrizeCountRecord

*振鑫-活动次数发放记录*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fZXUserID` | int |  |  |  |  | 关联T_ZX_User表ID |
| `fTag` | int |  |  |  |  | 活动标签，值1：618 新人注册抽奖活动 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `fStatus` | int |  |  | 否 | 0 | 0未使用，1已使用 |

## T_Base_Area_ZY_old

*行政区划编码表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cCode` | varchar(10) |  |  | 否 |  | 区域编码 |
| `cParentCode` | varchar(10) |  |  |  |  | 上级区域编码 |
| `cName` | nvarchar(50) |  |  | 否 |  | 区域名称 |
| `fLevel` | int |  |  |  | 0 | 区域级别 |

## T_ZX_Equity

*权益表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEquityID` | int |  |  | 否 | 0 | 权益表ID |
| `cGroupCode` | varchar(50) |  |  | 否 |  | 优惠券组编码 |
| `cGroupName` | nvarchar(50) |  |  |  |  | 优惠券组名称 |
| `fState` | tinyint |  |  | 否 | 0 | 状态 0禁用 1启用 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_XK_Dict

*线客字典详情表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `cTypeCode` | varchar(20) | 是 |  | 否 |  | 字典类型编码 |
| `cTypeName` | nvarchar(20) |  |  | 否 |  | 字典类型名称 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_PProductYz_PRCEnclosure

*医责险-渠道附件模板*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCID` | int |  |  |  |  | T_PProduct_PRCEnInsurance表ID |
| `fEnclosureID` | int |  |  |  |  | T_PProduct_Enclosure表ID |
| `cEnclosureName` | varchar(200) |  |  |  |  | 附件名称 |
| `cEnclosureCode` | varchar(50) |  |  |  |  | 附件编码 |
| `fIsUpLoad` | tinyint |  |  |  |  | 是否上传 |
| `fIsRequired` | tinyint |  |  |  |  | 是否必填 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cLastEditUser` | nvarchar(50) |  |  |  |  | 最后修改人 |
| `tLastEditTime` | datetime |  |  |  |  | 最后修改时间 |
| `fFlieType` | tinyint |  |  |  |  | 文件类型 1图片 2其他 |
| `cFileUrl` | varchar(300) |  |  |  |  | 附件模板url |
| `cFileTempUrl` | varchar(200) |  |  |  |  |  |
| `cDisplayName` | nvarchar(100) |  |  |  |  | 显示名称 |
| `cDesc` | nvarchar(100) |  |  |  |  | 备注 |
| `fSort` | int |  |  |  |  | 排序（正序） |

## T_PProduct_InsProgramme

*保险方案*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(50) |  |  |  |  | 内部名称 |
| `cDiaplayName` | nvarchar(50) |  |  |  |  | 客户端展示名称 |
| `fAmount` | decimal(18,2) |  |  |  |  | 总保费 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `fType` | int |  |  |  |  |  |
| `fSort` | int |  |  |  |  |  |

## T_PProductYz_PRCEnclosureGuarantee

*医责险-事故附件上传*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cEnclosureName` | nvarchar(50) |  |  |  |  | 附件名称 |
| `cEnclosureCode` | nvarchar(50) |  |  |  |  | 附件编码 |
| `fPRCEnclosureId` | int |  |  |  |  | 表id |
| `tCreateTime` | datetime |  |  |  |  | 创建时间 |
| `cLastEditUser` | nvarchar(50) |  |  |  |  | 最后修改人 |
| `tLastEditTime` | datetime |  |  |  |  | 最后修改时间 |
| `cUrl` | varchar(500) |  |  |  |  | 附件地址 |
| `cLocalUrl` | varchar(500) |  |  |  |  | ossUrl |
| `cName` | nvarchar(100) |  |  |  |  | 附件文件名称 |
| `fImageIsPush` | tinyint |  |  | 否 | 0 | 0:未推送 2：未打包，4：已打包，6：已推送 |
| `fMedicalAccidentID` | int |  |  | 否 |  |  |

## T_PProduct_Insurance

*农民工险种列表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cInsuranceName` | nvarchar(50) |  |  | 否 |  | 机构简称 |
| `cInsuranceFullName` | nvarchar(50) |  |  |  |  | 机构全称 |
| `cOrderLogo` | varchar(200) |  |  |  |  | 订单logo |
| `cInsuranceLogo` | varchar(200) |  |  |  |  | 保险logo |
| `tdate` | datetime |  |  | 否 | getdate() | 创建时间 |
| `cInvoiceTitle` | nvarchar(200) |  |  |  |  |  |
| `fInsuranceType` | tinyint |  |  |  | 0 |  |
| `fInsuranceCode` | nvarchar(50) |  |  |  |  |  |

## T_Enterprise_Info

*企业信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `CaID` | varchar(50) |  |  | 否 |  | CA企业序列号 |
| `cEnterpriseNo` | varchar(50) |  |  | 否 |  | 中心企业ID |
| `cEnterpriseName` | varchar(MAX) |  |  |  |  | 企业名称 |
| `cEnterpriseNameCode` | varchar(50) |  |  |  |  | 统一社会信用代码 |
| `cCorporationName` | nvarchar(20) |  |  |  |  | 法人姓名 |
| `cBank` | varchar(100) |  |  |  |  | 基本户开户行 |
| `cBankCardNo` | varchar(50) |  |  |  |  | 基本户账号 |
| `cLicenseUrl` | varchar(500) |  |  |  |  | 营业执照下载地址 |
| `cLicenseLocalUrl` | varchar(200) |  |  |  |  | 营业执照本地地址 |
| `CreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `UpdateTime` | datetime |  |  |  |  |  |
| `cIndustry` | nvarchar(20) |  |  |  |  | 所处行业 |
| `LicenseUpdateTime` | datetime |  |  |  |  | 营业执照更新时间 |
| `PRC_id` | int |  |  | 否 | 0 |  |
| `cCompanyAddress` | varchar(MAX) |  |  |  |  |  |
| `cContactUserName` | nvarchar(30) |  |  |  |  |  |
| `cContactUserTel` | varchar(50) |  |  |  |  |  |
| `cContactUserEmail` | varchar(50) |  |  |  |  |  |
| `cCompanyTel` | varchar(50) |  |  |  |  |  |
| `cAccountCertUrl` | varchar(250) |  |  |  |  |  |
| `cPwd` | varchar(100) |  |  |  |  |  |
| `fLoginErrCount` | int |  |  | 否 | 0 |  |
| `tLoginTime` | datetime |  |  |  |  |  |
| `fsignzt` | tinyint |  |  | 否 | 0 |  |
| `organizeAccountId` | varchar(50) |  |  |  |  |  |
| `cCorporationIDCard` | varchar(20) |  |  |  |  |  |
| `cCorporationPhone` | varchar(21) |  |  |  |  |  |
| `cCorporationCardType` | varchar(10) |  |  |  |  |  |
| `cContactUserCardType` | varchar(10) |  |  |  |  |  |
| `cContactUserIDCard` | varchar(50) |  |  |  |  |  |
| `Type` | tinyint |  |  | 否 | 1 |  |
| `IsVerified` | tinyint |  |  | 否 | 0 |  |
| `cAccountName` | nvarchar(50) |  |  |  |  |  |
| `cBankCode` | nvarchar(50) |  |  |  |  |  |
| `cEnterpriseNature` | varchar(20) |  |  |  |  |  |
| `cSheng` | varchar(10) |  |  |  |  |  |
| `cShi` | varchar(10) |  |  |  |  |  |
| `cQu` | varchar(10) |  |  |  |  |  |
| `fAuthManual` | int |  |  | 否 | 0 |  |
| `fAuthCount` | int |  |  | 否 | 0 |  |
| `tAuthTime` | datetime |  |  |  |  |  |
| `tRegTime` | datetime |  |  |  |  | 企业成立时间 |
| `fScale` | tinyint |  |  | 否 | 0 | 企业规模类型 0 无 1 大型企业 2 中型企业 3 小型企业 4 微型企业 |
| `fNature` | tinyint |  |  | 否 | 0 | 企业性质类型 0 无 1 民营 |
| `fIDCardEffect` | tinyint |  |  | 否 | 0 | 法人证件有效期类型 0 非长期有效 1 长期有效 |
| `tIDCardExp` | date |  |  |  |  | 法人证件有效期 |
| `cCorporationIDUrl` | varchar(500) |  |  |  |  | 法人证件url |
| `tExpTime` | date |  |  |  |  | 企业营业执照到期时间 |
| `cReportUrl` | nvarchar(500) |  |  |  |  |  |
| `cReportScore` | nvarchar(50) |  |  |  |  |  |

## T_GzZrx_PRCInsurance

*承保机构表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fInsuranceInfoID` | int |  |  | 否 | 0 | 金融机构id |
| `fInsuranceTypeID` | int |  |  | 否 | 0 | 险种id |
| `cInstCode` | varchar(50) |  |  | 否 |  | 承保机构编码 |
| `cInstName` | nvarchar(50) |  |  |  |  | 承保机构全称 |
| `cInstOrgCode` | varchar(20) |  |  |  |  | 承保机构信用代码 |
| `cCity` | nvarchar(50) |  |  |  |  | 承保机构所在地 省/市/区 |
| `cSheng` | nvarchar(20) |  |  |  |  | 承保机构所在地 省 |
| `cShi` | nvarchar(20) |  |  |  |  | 承保机构所在地 市 |
| `cQu` | nvarchar(20) |  |  |  |  | 承保机构所在地 区 |
| `cInstAddress` | nvarchar(100) |  |  |  |  | 承保机构详细地址 |
| `fPayType` | tinyint |  |  | 否 | 0 | 支付类型 0 对公支付 1 收银台支付 2 双支付模式 3 微信+余额支付 4 微信支付 5 余额支付 |
| `cAccount` | varchar(50) |  |  |  |  | 收款账号 |
| `cBank` | nvarchar(50) |  |  |  |  | 收款账户开户行 |
| `cBankUser` | nvarchar(50) |  |  |  |  | 账户户名 |
| `fSignType` | tinyint |  |  | 否 | 0 | 签章模式 0 强制线下签章 1 线下邮寄 2 ca签章 3 无需签章 4 非强制线下签章 |
| `fTbrMode` | tinyint |  |  | 否 | 0 | 投保人模式 |
| `fBbrMode` | tinyint |  |  | 否 | 0 | 被保人模式 |
| `fQuitType` | tinyint |  |  | 否 | 0 | 线上申请退保：0 无线上退保，1 线上退保（人工介入审核） |
| `cApiParameters` | varchar(200) |  |  |  |  | API出单接口对公 |
| `cJFApiParameters` | varchar(200) |  |  |  |  | API出单接口收银台 |
| `fInvoiceWay` | tinyint |  |  | 否 | 0 | 发票申请先后 0 后选发票 1 先选发票 |
| `fInvoiceApplyType` | tinyint |  |  | 否 | 0 | 发票支持类型 普票接口/专票线下 |
| `cInvoiceEmail` | varchar(200) |  |  |  |  | 保司专票接收邮箱 |
| `cPpExplain` | nvarchar(50) |  |  |  |  | 普票文字说明 |
| `cZpExplain` | nvarchar(50) |  |  |  |  | 专票文字说明 |
| `cPayTips` | nvarchar(1000) |  |  |  |  | 支付信息说明 |
| `cTips` | nvarchar(1000) |  |  |  |  | 温馨提示 |
| `cSignTips` | nvarchar(1000) |  |  |  |  | 签章页面提示 |
| `cQuitTips` | nvarchar(1000) |  |  |  |  | 退保温馨提示 |
| `cQuitExplain` | nvarchar(1000) |  |  |  |  | 退保说明 |
| `fState` | tinyint |  |  | 否 | 0 | 状态 0 禁用 1 启用 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `cBaoZhangTips` | nvarchar(1000) |  |  |  |  | 保障详情提示(货运险) |
| `cBkbHuoWuTips` | nvarchar(1000) |  |  |  |  | 不可保货物类型提示(货运险) |

## T_Invoice_Log

*发票申请记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `fType` | tinyint |  |  |  |  | 0普票电子发票，1普票纸质发票，2专票纸质发票 |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 企业名称 |
| `cEnterpriseNameCode` | varchar(50) |  |  |  |  | 统一社会信用代码 |
| `cProjectName` | nvarchar(1000) |  |  |  |  | 工程名称 |
| `cUser` | nvarchar(50) |  |  |  |  | 联系人 |
| `cUserPhone` | varchar(50) |  |  |  |  | 税务登录电话 |
| `cAddress` | nvarchar(100) |  |  |  |  | 税务登录地址 |
| `cEmail` | varchar(50) |  |  |  |  | 电子邮箱 |
| `cTel` | varchar(50) |  |  |  |  | 联系人手机号 |
| `cBank` | nvarchar(50) |  |  |  |  | 开户行 |
| `cAccount` | nvarchar(50) |  |  |  |  | 开户账号 |
| `fGuaranteeInfoID` | int |  |  |  |  | 保单表ID (其值为-1时，系振鑫批量申请发票记录) |
| `fProjectID` | int |  |  |  |  | 项目表ID |
| `fInvoiceAmount` | numeric(10,2) |  |  |  | 0 | 发票金额 |
| `fState` | tinyint |  |  |  |  | 状态：0待申请，1已申请且发票链接待保司写入，2开票成功发票链接已写入，3已推送，4推送失败 |
| `CreateTime` | datetime |  |  |  | getdate() |  |
| `tSubTime` | datetime |  |  |  |  |  |
| `cCompanyAddress` | nvarchar(100) |  |  |  |  | 发票邮寄地址 |
| `SignInvoice` | varchar(200) |  |  |  |  | 专票提醒确认函 |
| `invoiceUrl` | varchar(700) |  |  |  |  | 电子发票下载地址 |
| `invoiceCode` | varchar(50) |  |  |  |  | 发票代码 |
| `invoiceNo` | varchar(50) |  |  |  |  | 发票号码 |
| `ErrMsg` | nvarchar(150) |  |  |  |  | 在线开票失败原因 |
| `SignInvoiceLocalUrl` | varchar(200) |  |  |  |  |  |
| `cTaxPayerNo` | varchar(50) |  |  |  |  |  |
| `cAuditUserName` | nvarchar(20) |  |  | 否 | '' |  |
| `cAuditMessage` | nvarchar(50) |  |  | 否 | '' |  |
| `fCustomerOffline` | tinyint |  |  | 否 | 0 |  |
| `fSendEmail` | tinyint |  |  | 否 | 0 |  |
| `emailId` | int |  |  | 否 | 0 |  |
| `cBidName` | nvarchar(600) |  |  |  |  | 标段名称 |
| `fFromType` | tinyint |  |  | 否 | 0 | 申请来源 0 默认 1 智慧云闪票H5 2 振鑫小程序 |
| `fIgnoreError` | tinyint |  |  | 否 | 0 | 核心后台异常统计时，忽略不统计 |
| `fJGState` | tinyint |  |  | 否 | 0 | 金融机构发票状态 0 已申请发票 1 已推送待开具 2 已开具 |
| `ZpPushState` | tinyint |  |  | 否 | 0 | 专票状态（不维护fstate）：0待申请，1已申请待保司写入，2开票成功信息已写入，3已推送，4推送失败 |
| `PolicyNos` | nvarchar(500) |  |  |  |  | 批量申请的关联订单组合，逗号隔开。此时 fGuaranteeInfoID=0 |
| `cRemarks` | nvarchar(500) |  |  |  |  | 备注 |
| `instname` | nvarchar(50) |  |  |  |  | 承保机构全称 |
| `fZXUserID` | int |  |  |  |  | 振鑫用户ID（振鑫专用） |

## T_Base_Area_CT

*行政区划编码表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cCode` | varchar(10) |  |  | 否 |  | 区域编码 |
| `cParentCode` | varchar(10) |  |  |  |  | 上级区域编码 |
| `cName` | nvarchar(50) |  |  | 否 |  | 区域名称 |
| `fLevel` | int |  |  |  | 0 | 区域级别 |

## T_ZX_ProductPartners

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fProductInfoID` | int |  |  | 否 | 0 | T_ZX_ProductInfo表ID |
| `fSort` | int |  |  | 否 |  |  |
| `cPartnerPic` | varchar(200) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_PProduct_Attachment

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cAttachmentName` | varchar(200) |  |  |  |  |  |
| `cAttachmentCode` | varchar(50) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cLastEditUser` | nvarchar(50) |  |  |  |  | 最后修改人 |
| `tLastEditTime` | datetime |  |  |  |  | 最后修改时间 |
| `fFlieType` | tinyint |  |  |  |  | 文件类型 1图片 2文件 3压缩包 |
| `fTag` | tinyint |  |  |  |  | 0企业信息附件配置，1项目信息附件配置 |

## YanShiTemp

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cInsuranceCompany` | nvarchar(10) |  |  | 否 |  |  |
| `cPGPolicyUrl` | varchar(500) |  |  | 否 |  |  |

## T_Insurance_FileTemplate

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fBaseID` | int |  |  |  |  |  |
| `cName` | nvarchar(50) |  |  |  |  |  |
| `cFileNumber` | varchar(50) |  |  |  |  |  |
| `cFileUrl` | varchar(200) |  |  |  |  |  |
| `fFileSaveType` | tinyint |  |  |  |  |  |
| `CreateTime` | datetime |  |  |  |  |  |
| `fOrder` | int |  |  |  |  |  |
| `cPosX` | varchar(30) |  |  |  |  |  |
| `cPosY` | varchar(30) |  |  |  |  |  |
| `cRemarks` | nvarchar(MAX) |  |  |  |  |  |
| `cProductTypeNo` | varchar(30) |  |  |  |  |  |
| `cProductNo` | varchar(30) |  |  |  |  |  |
| `fPosPage` | tinyint |  |  |  |  |  |
| `cContent` | nvarchar(2000) |  |  |  |  |  |
| `cFilePreviewUrl` | varchar(500) |  |  |  |  | 预览地址（振鑫手机端展示用png地址） |
| `fDaysType` | tinyint |  |  | 否 | 1 | 担保天数类型（1：固定天数；2：用户输入） |
| `fDays` | int |  |  | 否 | 0 | 担保天数 |
| `fExtendDays` | int |  |  | 否 | 0 | 扩展天数（担保小程序用到） |
| `cShowItems` | varchar(20) |  |  | 否 | '0,0,0,0' | 显示信息0：不显示；1：显示。（4个段位分别表示：项目名称，项目编号，标段名称，标段编号） |

## T_GzZrx_Enterprise

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 企业名称 |
| `cEnterpriseNameCode` | nvarchar(64) |  |  |  |  | 统一社会信用代码 |
| `cCompanyTel` | nvarchar(20) |  |  |  |  | 税务登记电话 |
| `cCompanyAddress` | nvarchar(100) |  |  |  |  | 税务登记地址（营业执照注册地址） |
| `tRegTime` | datetime |  |  |  |  | 成立日期 |
| `cLegalUserName` | nvarchar(30) |  |  |  |  | 企业法定代表人 |
| `cContactUserName` | nvarchar(30) |  |  |  |  | 联系人 |
| `cContactUserTel` | varchar(50) |  |  |  |  | 联系人手机号 |
| `cContactUserEmail` | varchar(50) |  |  |  |  | 联系人邮箱 |
| `cContactUserAddress` | nvarchar(100) |  |  |  |  | 收件地址 |
| `UpdateTime` | datetime |  |  |  |  |  |
| `cUserID` | varchar(50) |  |  |  |  | 录入的用户ID，对应T_GzZrx_Users表ID |
| `cBank` | nvarchar(100) |  |  |  |  |  |
| `cBankCardNo` | varchar(50) |  |  |  |  |  |
| `cBusinessType` | nvarchar(20) |  |  |  |  | 行业类型代码 |
| `tStartDate` | date |  |  |  |  | 营业执照有效起期 |
| `tEndDate` | date |  |  |  |  | 营业执照有效止期 |
| `tCreateDate` | datetime |  |  |  | getdate() | 创建时间 |

## T_PProductYz_Result

*医责险-确责记录*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fGuaranteeId` | int |  |  | 否 |  | 保单表id   T_PProductYz_Guarantee |
| `fMedicalAccidentId` | int |  |  | 否 |  | 事故表id   T_PProductYz_MedicalAccident |
| `fType` | tinyint |  |  | 否 |  | 调解类型（1：医院调节；2：医疗纠纷人民调节委员会调节；3：人民法院厅外调节；4：人民法院宣判） |
| `fResultType` | tinyint |  |  | 否 |  | 调解结果（1：调解成功，院方全责；2：调解成功，院方主要责任；3：调解成功，院方次要责任；4：调解成功，院方轻微责任；5：调解成功，院方无责；6：调解失败） |
| `tDate` | datetime |  |  | 否 |  | 调解时间 |
| `cGroupName` | nvarchar(50) |  |  | 否 |  | 调解机构 |
| `cName` | nvarchar(50) |  |  |  |  | 调解人 |
| `cPhone` | varchar(20) |  |  |  |  | 调解人联系方式 |
| `cAddress` | nvarchar(200) |  |  |  |  | 调解机构地址 |
| `cContent` | nvarchar(500) |  |  | 否 |  | 调解结果摘要 |
| `cUrl` | nvarchar(200) |  |  |  |  | 附件地址 |
| `tCreateDate` | datetime |  |  |  | getdate() |  |
| `cUserName` | nvarchar(50) |  |  |  |  | 录入人 |
| `cNo` | varchar(50) |  |  |  |  | 确责记录编号 |
| `tEndDate` | datetime |  |  | 否 |  | 调解时间(止) |

## T_NJDT_ShowInfoTemplate

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(50) |  |  |  |  | 字段名称 |
| `cCode` | varchar(50) |  |  |  | (0) | 编码 |

## T_PProduct_ProductInfo

*农民工项目表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cProjectNo` | nvarchar(200) |  |  |  |  | 项目编号 |
| `cProjectName` | nvarchar(200) |  |  |  |  | 项目名称 |
| `cContractNo` | varchar(50) |  |  |  |  | 合同编号 |
| `cContractName` | nvarchar(50) |  |  |  |  | 合同名称 |
| `cOwnerUnit` | nvarchar(1000) |  |  |  |  | 招标单位 |
| `cOwnerUnitCode` | varchar(1000) |  |  |  |  | 招标单位统一社会信用代码，项目归属机构代码 |
| `provinceName` | nvarchar(20) |  |  |  |  | 省 |
| `cityName` | nvarchar(20) |  |  |  |  | 市 |
| `areaName` | nvarchar(20) |  |  |  |  | 区 |
| `fProjectAmount` | decimal(18,2) |  |  |  | 0 | 项目金额、工程预计合同造价 |
| `fStartTime` | datetime |  |  |  |  | 计划开工日期 |
| `plannedDuration` | numeric(10,1) |  |  |  | 0 | 计划工期 |
| `plannedUnit` | nvarchar(10) |  |  |  | N'天' | 计划工期单位：天OR年 |
| `cQualification` | nvarchar(20) |  |  |  |  | 施工资质 |
| `tMAmountTime_s` | datetime |  |  |  |  | 保证金有效期限开始时间 |
| `tMAmountTime_e` | datetime |  |  |  |  | 保证金有效期限结束时间 |
| `cProjectAddress` | nvarchar(200) |  |  |  |  | 项目地址 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |
| `fzt` | tinyint |  |  |  | 0 | 状态，0正常，1异常 |
| `platformCode` | varchar(50) |  |  |  |  | 平台代码 |
| `cUserID` | varchar(50) |  |  |  |  | 录入的用户ID，对应T_PProduct_Admin表ID |
| `fBusinessType` | tinyint |  |  |  | 0 | 最近业务类型,0无，1现金缴纳，2保险保函，3银行保函，4担保保函 |
| `fMarginAmount` | decimal(18,2) |  |  |  | 0 | 保证金 |
| `fFromType` | tinyint |  |  |  | 0 | 项目来源，0录入，1中心推送 |
| `fDelayState` | tinyint |  |  |  | 0 | 最近延期状态，0无，1待办理延期，2延期已受理（已延期），6无需延期 |
| `tLastDelayTime` | datetime |  |  |  |  | 最近延期时间，初始默认值同tMAmountTime_e |
| `cNewGuid` | varchar(50) |  |  |  |  | 唯一性标识 |
| `fEnterpriseInfoID` | int |  |  |  | 0 | 对应企业表ID |
| `fBusinessCount` | int |  |  |  | 0 | 保证金缴纳方式次数 |
| `cBidNoticeNo` | varchar(50) |  |  |  |  | 中标通知书编号 |
| `cBidId` | nvarchar(100) |  |  |  |  | 标段ID |
| `cBidName` | nvarchar(150) |  |  |  |  | 标段名称 |
| `cBidType` | nvarchar(30) |  |  |  |  | 招标类型 |
| `tBidWinTime` | datetime |  |  |  |  | 中标时间 |
| `cPostalAddress` | nvarchar(200) |  |  |  |  | 业主联系地址 |
| `cAccName` | nvarchar(50) |  |  |  |  | 业主联系人 |
| `cMobile` | varchar(30) |  |  |  |  | 业主联系电话 |
| `cKindName` | varchar(300) |  |  |  |  | 合同履约保函 |
| `cManageCom` | varchar(100) |  |  |  |  | 归属机构代码 |
| `cBusinessSite` | varchar(300) |  |  |  |  | 建设地点 |
| `cProPic` | varchar(200) |  |  |  |  | 产品图片 |
| `cDes` | nvarchar(3000) |  |  |  |  | 产品内容 |
| `cIntroduction` | nvarchar(100) |  |  |  |  | 产品简介 |
| `InsuredUnitNature` | nvarchar(10) |  |  |  |  |  |
| `InsuredProvince` | nvarchar(10) |  |  |  |  |  |
| `InsuredCity` | nvarchar(10) |  |  |  |  |  |
| `InsuredArea` | nvarchar(10) |  |  |  |  |  |
| `cUnitNature` | nvarchar(30) |  |  |  |  |  |
| `cProvince` | nvarchar(30) |  |  |  |  |  |
| `cCity` | nvarchar(30) |  |  |  |  |  |
| `cArea` | nvarchar(30) |  |  |  |  |  |
| `cProjectType` | nvarchar(30) |  |  |  |  |  |
| `tPlanStartTime` | datetime |  |  |  |  |  |
| `tPlanEndTime` | datetime |  |  |  |  |  |
| `cDismantle` | nvarchar(50) |  |  |  |  |  |
| `tContractSignTime` | datetime |  |  |  |  |  |
| `tDeliveryTime` | datetime |  |  |  |  |  |
| `cCargoStandard` | nvarchar(50) |  |  |  |  |  |
| `cWarrantyPeriod` | nvarchar(30) |  |  |  |  |  |
| `cInsuranceTypeNo` | nvarchar(50) |  |  |  |  |  |
| `cOwnerContactUserName` | nvarchar(100) |  |  |  |  |  |
| `cOwnerContactUserPhone` | nvarchar(100) |  |  |  |  |  |
| `cProjectTypeName` | nvarchar(50) |  |  |  |  |  |
| `provinceCode` | nvarchar(20) |  |  |  |  |  |
| `cityCode` | nvarchar(20) |  |  |  |  |  |
| `areaCode` | nvarchar(20) |  |  |  |  |  |
| `cPostalCode` | varchar(50) |  |  |  |  |  |
| `cSGContractNo` | varchar(50) |  |  |  |  |  |
| `fEndTime` | datetime |  |  |  |  |  |
| `cProArea` | nvarchar(100) |  |  |  |  |  |
| `cSGNo` | varchar(50) |  |  |  |  |  |
| `cSGApproveDate` | datetime |  |  |  |  |  |
| `tQXZRDate_begin` | datetime |  |  |  |  |  |
| `tQXZRDate_end` | datetime |  |  |  |  |  |
| `ftQXZRDuration` | int |  |  |  |  |  |
| `cSignNo` | nvarchar(100) |  |  |  |  |  |
| `fIsPush` | tinyint |  |  |  | 0 | 是否推送（0：未推送；1：已推送） |
| `tPushDate` | datetime |  |  |  |  | 推送时间 |
| `wxareaCode` | nvarchar(20) |  |  |  |  | 浙大网新地区编码，（山西农民工工资监管项目） |
| `cContractType` | nvarchar(50) |  |  |  |  | 工程合同类型 1	施工总承包, 2	工程总承包 |
| `cBudgetAmount` | decimal(18,6) |  |  |  |  | 财政预算 （元） |
| `isUseBudgetAmount` | bit |  |  |  |  | 是否使用财政预算资金 0是 1否 |
| `zcbdanweiname` | nvarchar(200) |  |  |  |  | 总承包单位名称 |
| `zcbunitorgnum` | nvarchar(50) |  |  |  |  | 总承包单位统一社会信用代码 |
| `cProjectCategory` | nvarchar(50) |  |  |  |  | 项目类别（自贡中心传） |

## T_PProduct_IntegratedPRCAttachment

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fIntegratedPRCid` | int |  |  |  |  | T_PProduct_IntegratedPRC表ID |
| `fAttachmentID` | int |  |  |  |  | T_PProduct_Enclosure表ID |
| `cAttachmentName` | varchar(200) |  |  |  |  | 附件名称 |
| `cAttachmentCode` | varchar(150) |  |  |  |  | 附件编码 |
| `fIsUpLoad` | tinyint |  |  |  |  | 是否上传 |
| `fIsRequired` | tinyint |  |  |  |  | 是否必填 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cLastEditUser` | nvarchar(50) |  |  |  |  | 最后修改人 |
| `tLastEditTime` | datetime |  |  |  |  | 最后修改时间 |
| `fFlieType` | tinyint |  |  |  |  | 文件类型 1图片 2其他 |
| `cFileTempUrl` | varchar(200) |  |  |  |  |  |
| `cDisplayName` | nvarchar(100) |  |  |  |  |  |
| `cDesc` | nvarchar(100) |  |  |  |  |  |
| `fSort` | int |  |  |  |  |  |

## T_Insurance_FileTemplateBase

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fInsuranceID` | int |  |  | 否 |  |  |
| `cName` | nvarchar(50) |  |  |  |  |  |
| `fIsDefault` | tinyint |  |  | 否 |  |  |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cCode` | varchar(30) |  |  |  |  |  |

## T_ZX_UserEnEquity

*用户和权益关联表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fUserID` | int |  |  | 否 | 0 | 用户T_ZX_User表id |
| `fEquityID` | int |  |  | 否 | 0 | 权益T_ZX_Equity表id |
| `tEffectiveTime` | datetime |  |  | 否 | getdate() | 权益生效时间 |
| `tExpireTime` | datetime |  |  | 否 | getdate() | 权益失效时间 |
| `fState` | tinyint |  |  | 否 | 0 | 默认0 未使用 1 待发放 2 已使用 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `tApplyTime` | datetime |  |  |  |  | 申请使用时间 |
| `fEquityCouponGroupID` | int |  |  | 否 | 0 | 兑换产品T_ZX_EquityCouponGroup表id |
| `cZmclUrl` | varchar(200) |  |  |  |  | 证明材料 |
| `cRemark` | nvarchar(200) |  |  |  |  | 备注 |
| `fChuliState` | tinyint |  |  | 否 | 0 | 处理状态 0 未处理 1 已处理 |
| `tChuliTime` | datetime |  |  |  |  | 处理时间 |

## T_Policy_FreeIDs

*后台人工去限制出单ID记录表，比如联银*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `cInsuranceCompany` | nvarchar(20) |  |  |  |  | 金融机构 |
| `fGuaranteeID` | int |  |  |  | 0 | 关联T_Guarantee_Info表ID |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cUser` | nvarchar(50) |  |  |  |  | 操作人 |
| `cRemark` | nvarchar(500) |  |  |  |  | 备注 |
| `fZt` | tinyint |  |  |  | 0 | 状态，0有效，1无效 |

## T_PaymentSystem_Insurance

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cNumber` | varchar(50) | 是 |  | 否 |  | 保险公司编号 |
| `cShortName` | nvarchar(50) |  |  |  |  | 保险公司简称 |
| `cFullName` | nvarchar(50) |  |  |  |  | 保险公司全称 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |

## T_PProductYz_RoleMenus

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Id` | int | 是 | 是 | 否 |  |  |
| `tCreateTime` | datetime |  |  | 否 |  |  |
| `IsDeleted` | bit |  |  | 否 |  |  |
| `MenuId` | int |  |  |  |  |  |
| `RoleId` | int |  |  |  |  |  |

## T_PProduct_ConstructionGrade

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 |  | 否 |  |  |
| `cConstructionGrade` | nvarchar(10) |  |  |  |  |  |

## T_PProduct_IntegratedCommodity

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCID` | int |  |  |  |  | 一体化渠道ID |
| `fProductID` | int |  |  |  |  | 产品ID |
| `cProductCode` | nvarchar(50) |  |  |  |  | 产品编码 |
| `cProductFullName` | nvarchar(50) |  |  |  |  | 产品名称 |
| `cProductShortName` | nvarchar(50) |  |  |  |  | 产品简称 |
| `fOrderWaringDay` | int |  |  |  |  | 保单到期预警天数 |
| `fHandleWaringDay` | int |  |  |  |  | 新缴未备案预警天数 |
| `fRenewalWaringDay` | int |  |  |  |  | 续缴未备案预警天数 |
| `fMakeUpWaringDay` | int |  |  |  |  | 补缴未备案预警天数 |
| `fFinishedWaringDay` | int |  |  |  |  | 完工/延期未确认预警天数 |
| `fBuyWay` | int |  |  |  |  | 购买限制 |
| `fClaimWay` | int |  |  |  |  | 理赔申请方式 |
| `fQuitWay` | int |  |  |  |  | 退保方式 |
| `fIsSupervise` | tinyint |  |  |  |  | 是否监管 |
| `fSuperviseID` | int |  |  |  |  | 监管渠道ID |
| `cOnlineFlowCharUrl` | nvarchar(200) |  |  |  |  | 线上出单流程图 |
| `cOfflineFlowCharUrl` | nvarchar(200) |  |  |  |  | 线下办理流程图 |
| `fIsAutoPremium` | tinyint |  |  |  |  | 是否需要自动计算保证金预估金额 |
| `fOnlinePayType` | tinyint |  |  |  |  | 线上办理支持的缴纳类型 |
| `fOfflinePayType` | tinyint |  |  |  |  | 线下办理支持的缴纳类型 |
| `fNecessaryRate` | tinyint |  |  | 否 |  | 线下出单费率是否必填  0否 1是 |
| `fNecessaryPremium` | tinyint |  |  |  |  | 线下出单费用（保费）是否必填  0否 1是 |
| `fOfflineInsuranceType` | tinyint |  |  |  |  | 线下出单机构控制  1市级及市级以下机构出单 2 区县级机构出单 |
| `fOfflinePolicyType` | tinyint |  |  |  |  | 线下出单凭证类型  1金融机构自有格式 2金融机构自有格式 + 人社统一凭证各一份 3金融机构自有格式附人社统一凭证  共一份 4人社统一格式凭证 |
| `fLabel` | int |  |  |  |  | 商品标签 |
| `fState` | tinyint |  |  |  |  | 开通状态 |
| `fHotWeight` | int |  |  |  |  | 热度权重 |
| `fClickNum` | float |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cOnlinePayType` | nvarchar(200) |  |  |  |  | 线上办理支持的缴纳类型 |
| `cOfflinePayType` | nvarchar(200) |  |  |  |  | 线下办理支持的缴纳类型 |
| `cAbout` | text |  |  |  |  | 产品说明 |
| `cBuyProcess` | text |  |  |  |  | 购买流程 |
| `cCommonProblem` | text |  |  |  |  | 常见问题 |

## T_Insurance_InfoDoSign

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `InsuranceName` | nvarchar(50) | 是 |  | 否 |  | 保险公司名称 |
| `enterpriseName` | nvarchar(50) |  |  |  |  | 机构全称 |
| `socialCreditCode` | varchar(50) |  |  |  |  | 机构统一社会信用代码 |
| `organizeAccountId` | varchar(50) |  |  |  |  | 机构签章代码 |
| `sealId` | varchar(50) |  |  |  |  | 企业章模id |
| `userName` | nvarchar(20) |  |  |  |  | 法人姓名 |
| `userIDnumber` | varchar(50) |  |  |  |  | 法人身份证号 |
| `userOrganizeAccountId` | varchar(50) |  |  |  |  | 法人签章代码 |
| `userSealId` | varchar(50) |  |  |  |  | 法人章模id |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |

## T_GzZrx_InsuranceFile

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fInsuranceID` | int |  |  | 否 | 0 |  |
| `cName` | nvarchar(50) |  |  |  |  |  |
| `fIsDefault` | tinyint |  |  | 否 | 0 |  |
| `fInsuranceTypeID` | int |  |  | 否 | 0 |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_ZX_ProductInquiryExtend

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Id` | int |  | 是 | 否 |  |  |
| `cInquiryGuid` | varchar(50) |  |  |  |  |  |
| `userid` | nvarchar(50) |  |  |  |  |  |
| `cBank` | nvarchar(100) |  |  |  |  | 基本户开户行名称 |
| `cBankCardNo` | varchar(100) |  |  |  |  | 基本户卡号 |
| `cBankAccountName` | nvarchar(100) |  |  |  |  |  |
| `guarantee_type` | int |  |  |  |  | 投保类型， 必填 0:投标履约 1:施工履约保函 2:农民工工资保函 3:工程款支付保函 4:工程质量保证保函 5:安全生产责任险 默认 0 |
| `tBidWinTime` | datetime |  |  |  |  | 中标结果公告发布时间 |
| `cProjectNo` | nvarchar(200) |  |  |  |  | 项目编号 |
| `bzjenddate` | datetime |  |  |  |  | 保证金缴纳截止时间 |
| `tPublishTime` | datetime |  |  |  |  | 项目发布时间 |
| `plannedDuration` | nvarchar(50) |  |  |  |  | 计划工期,有单位，如23（ 日历天）. （日历天） 、 （ 日历周） 等， 有可能 "-" |
| `projectPrice` | nvarchar(50) |  |  |  |  | 项目预计造价 可能为"-" |
| `projectAddress` | nvarchar(800) |  |  |  |  | 项目建设地点 |
| `projectType` | varchar(10) |  |  |  |  | 招标项目类别,必填,枚举： 建筑设计-A01;市政设计-A02;园林绿化-A98;公路-A03;采购-A04;水运-A06;其他-A99 |
| `fFender_expire` | int |  |  |  |  | 投保有效期 天 |
| `cBiddingNoticeUrl` | varchar(MAX) |  |  |  |  | 招标公告地址 |
| `cBiddingDocUrl` | varchar(MAX) |  |  |  |  | 招标文件地址 |
| `cOwnerUnit` | nvarchar(50) |  |  |  |  |  |
| `cOwnerUnitCode` | nvarchar(50) |  |  |  |  |  |
| `cOwnerContactUserTel` | varchar(50) |  |  |  |  |  |
| `cOwnerContactUserName` | varchar(50) |  |  |  |  |  |
| `cOwnerBankCardNo` | varchar(50) |  |  |  |  |  |
| `cOwnerBank` | varchar(50) |  |  |  |  |  |
| `cOwnerAccount` | varchar(50) |  |  |  |  |  |
| `cOwnerCompanyTel` | varchar(50) |  |  |  |  | 招标人公司联系电话 |
| `cOwnerAddress` | nvarchar(100) |  |  |  |  |  |
| `cApprovalCode` | nvarchar(100) |  |  |  |  | 项目审批编号 |
| `cContactUserName` | nvarchar(30) |  |  |  |  | 联系人名称 |
| `cCompanyAddress` | varchar(100) |  |  |  |  | 企业地址 |
| `cEmail` | varchar(50) |  |  |  |  |  |
| `cCorporationName` | nvarchar(20) |  |  |  |  | 法人姓名 |
| `cCorporationIDCard` | nvarchar(20) |  |  |  |  |  |
| `cCorporationPhone` | nvarchar(50) |  |  |  |  |  |
| `cLicenseUrl` | varchar(1000) |  |  |  |  | 营业执照地址 |
| `cEsignUrl` | nvarchar(300) |  |  |  |  | 签章地址 |
| `cProjectAgency` | nvarchar(1000) |  |  |  |  | 招标代理机构名称 |
| `tCreateTime` | datetime |  |  |  | getdate() |  |
| `tPlannedStartDate` | datetime |  |  |  |  | 计划开工日期 |
| `tPlannedEndDate` | datetime |  |  |  |  | 计划完工日期 |
| `cProjectTypeName` | nvarchar(30) |  |  |  |  | 项目类型中文名称 |
| `fBuildingArea` | decimal(18,2) |  |  |  |  | 建筑面积 |

## T_Invoice_Info

*发票信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `fType` | tinyint |  |  |  | 0 | 0普票电子发票，1普票纸质发票，2专票纸质发票 |
| `cUser` | nvarchar(20) |  |  |  |  | 联系人 |
| `cUserPhone` | varchar(50) |  |  |  |  | 税务登记电话 |
| `cAddress` | nvarchar(100) |  |  |  |  | 税务登记地址 |
| `cEmail` | varchar(50) |  |  |  |  | 电子邮箱 |
| `cTel` | varchar(50) |  |  |  |  | 联系人手机号 |
| `cBank` | nvarchar(30) |  |  |  |  | 开户行 |
| `cAccount` | nvarchar(30) |  |  |  |  | 开户账号 |
| `CreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `cCompanyAddress` | nvarchar(100) |  |  |  |  | 发票邮寄地址 |
| `SignInvoice` | varchar(200) |  |  | 否 | '' | 专票提醒确认函 |
| `isSignInvoice` | tinyint |  |  | 否 | 0 | 是否已签章，0：否，1：是 |
| `cTaxPayerNo` | varchar(50) |  |  |  |  |  |
| `fIsZzsTaxPayer` | tinyint |  |  |  | 1 |  |
| `cTaxPayerFile` | varchar(200) |  |  |  | NULL |  |

## T_Insurance_Info

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `InsuranceName` | nvarchar(50) | 是 |  | 否 |  | 保险公司名称 |
| `enterpriseName` | nvarchar(50) |  |  |  |  | 机构全称 |
| `socialCreditCode` | varchar(50) |  |  |  |  | 机构统一社会信用代码 |
| `organizeAccountId` | varchar(50) |  |  |  |  | 机构签章代码 |
| `sealId` | varchar(50) |  |  |  |  | 企业章模id |
| `userName` | nvarchar(20) |  |  |  |  | 法人姓名 |
| `userIDnumber` | varchar(50) |  |  |  |  | 法人身份证号 |
| `userOrganizeAccountId` | varchar(50) |  |  |  |  | 法人签章代码 |
| `userSealId` | varchar(50) |  |  |  |  | 法人章模id |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |

## T_PProductYz_Roles

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Id` | int | 是 | 是 | 否 |  |  |
| `tCreateTime` | datetime |  |  | 否 |  | 创建时间 |
| `Description` | nvarchar(50) |  |  |  |  | 角色描述 |
| `IsDeleted` | bit |  |  | 否 |  | 是否已删除 |
| `IsSuperRole` | bit |  |  | 否 |  | 是否是超级管理员 |
| `Name` | nvarchar(20) |  |  | 否 |  |  |

## T_Base_Nature

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 |  | 否 |  |  |
| `cCode` | varchar(10) |  |  | 否 |  |  |
| `cName` | nvarchar(20) |  |  | 否 |  |  |

## T_GzZrx_interface

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fPrcEnsuranceId` | int |  |  |  |  | T_GzZrx_PRCInsurance.ID |
| `Insurance_id` | int |  |  |  |  | T_Insurance_Info.ID |
| `ZfUrl` | varchar(200) |  |  |  |  | 生成支付链接地址 |
| `ZfCloseUrl` | varchar(200) |  |  |  |  | 支付关单URL |
| `ZfCallBackUrl` | varchar(200) |  |  |  |  | 支付回调地址 |
| `CdUrl` | varchar(200) |  |  |  |  | 出单地址 |
| `PdUrl` | varchar(200) |  |  |  |  | 批单地址 |
| `FpUrl` | varchar(200) |  |  |  |  | 发票地址 |
| `BdxzUrl` | varchar(200) |  |  |  |  | 保单下载地址 |
| `DdgbUrl` | varchar(200) |  |  |  |  | 订单关闭地址 |
| `CdztcxUrl` | varchar(200) |  |  |  |  | 出单状态查询url |
| `TbUrl` | varchar(200) |  |  |  |  | 退保地址 |
| `Api` | varchar(200) |  |  |  |  | 保司出单参数 |
| `aeskey` | varchar(200) |  |  |  |  | 对称密钥 |
| `sm4Key` | varchar(200) |  |  |  |  |  |
| `pubKey` | varchar(200) |  |  |  |  | 平台公钥 |
| `priKey` | varchar(200) |  |  |  |  | 平台私钥 |
| `merchantPubKey` | varchar(200) |  |  |  |  | 商户公钥 |
| `merchantPriKey` | varchar(200) |  |  |  |  | 商户私钥 |
| `OSS_Url` | varchar(200) |  |  |  |  | OOS前缀地址 |
| `FileAddree` | varchar(200) |  |  |  |  | 文件存储系统接口 |
| `isPg` | int |  |  |  |  | 0 明文  1密文 |
| `PayWay` | varchar(4) |  |  |  |  | 见费模式 |
| `Remarks` | varbinary |  |  |  |  | 备注说明 |

## T_PProductYz_OperationLog

*医责险操作记录*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cAccount` | nvarchar(50) |  |  |  |  | 账号 |
| `cCompany` | nvarchar(50) |  |  |  |  | 所属公司 |
| `cName` | nvarchar(50) |  |  |  |  | 姓名 |
| `cType` | nvarchar(50) |  |  |  |  | 操作类型 |
| `tCreateDate` | datetime |  |  |  | getdate() | 添加时间 |

## T_PProduct_IntegratedCommodityLink

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnInsuranceID` | int |  |  |  |  | 一体化渠道ID |
| `fInsuranceID` | int |  |  |  |  | fType=1 对应T_PProduct_InvoiceInfo表ID fType=2 对应T_PProduct_OfflineInsuranceInfo ID |
| `fType` | int |  |  |  |  | 类型 1线上 2线下 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cName` | nvarchar(50) |  |  |  |  |  |
| `cPhone` | nvarchar(50) |  |  |  |  |  |
| `cCustomerServicePhone` | nvarchar(50) |  |  |  |  |  |
| `cPRCCode` | nvarchar(50) |  |  |  |  |  |

## T_Esign_Apply

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cDDNo` | varchar(100) |  |  |  |  | 订单审批号 |
| `cUsage` | nvarchar(200) |  |  |  |  | 签章用途 |
| `fIsSend` | tinyint |  |  |  | 0 | 是否邮箱发送  0：否；1：是 |
| `fromEmail` | nvarchar(50) |  |  |  |  | 发件邮箱 |
| `cTitle` | nvarchar(50) |  |  |  |  | 邮箱标题 |
| `fJSInfoId` | int |  |  |  | 0 | 保司结算邮箱 对应的结算对象id |
| `cCCMail` | nvarchar(500) |  |  |  |  | 抄送邮箱 |
| `cAttachUrls` | nvarchar(3000) |  |  |  |  | 无需签章附件 |
| `fStatus` | tinyint |  |  |  | 0 | 签章状态（0：待签章；1：签章成功；2：已作废） |
| `fIsPush` | tinyint |  |  |  | 0 | 是否推送（0：未推送；1：推送中；2：推送成功） |
| `tPushTime` | datetime |  |  |  |  | 推送时间 |
| `tCreateDate` | datetime |  |  |  | getdate() | 创建时间 |
| `cApplyUser` | nvarchar(50) |  |  |  |  | 申请人 |
| `cAuthUser` | nvarchar(50) |  |  |  |  | 审核人 |
| `tAuthTime` | datetime |  |  |  |  | 审核时间 |
| `fCount` | int |  |  |  |  | 签章文件数 |
| `cError` | nvarchar(50) |  |  |  |  |  |
| `fIsTmp` | tinyint |  |  |  | 1 | 是否草稿（1：草稿；0：正式） |
| `cApplyUserId` | nvarchar(100) |  |  |  |  |  |
| `cAuthUserId` | nvarchar(100) |  |  |  |  |  |
| `fFrom` | tinyint |  |  | 否 | 0 | 来源（0：内部电子用章；1：国科） |
| `tCancelTime` | datetime |  |  |  |  |  |
| `cCancelUser` | nvarchar(50) |  |  |  |  |  |
| `cCancelUserId` | nvarchar(50) |  |  |  |  |  |
| `fIsDownloadFile` | tinyint |  |  | 否 | 0 |  |

## T_ZX_ChannelLeveltwo

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fChannelID` | int |  |  | 否 | 0 | T_ZX_Channel表ID |
| `cLeveltwoCode` | varchar(50) |  |  |  |  | 二级渠道编码 |
| `cLeveltwoName` | nvarchar(50) |  |  |  |  | 二级渠道名称 |
| `cLeveltwoShortName` | nvarchar(20) |  |  |  |  | 二级渠道简称 |
| `cLeveltwoAttributionUser` | nvarchar(10) |  |  |  |  | 二级渠道业务归属 |
| `cLeveltwoQrCodeUrl` | varchar(200) |  |  |  |  | 二级渠道二级码 |
| `fState` | tinyint |  |  | 否 | 0 | 状态 0禁用 1启用 |
| `cRemark` | nvarchar(200) |  |  |  |  | 备注 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |
| `cQiWeiUrl` | varchar(200) |  |  |  |  | 企微图片 |

## T_ZX_GoodsType

*振鑫小程序-商品类别表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(20) |  |  |  |  | 类别名称 |
| `cDes` | nvarchar(150) |  |  |  |  | 分类描述 |
| `fIsDeleted` | tinyint |  |  | 否 | 0 | 是否删除，默认0否，1是 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `cAuditUserName` | nvarchar(20) |  |  |  |  | 后台添加审核人 |

## T_Login_Black

*登陆黑名单表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `blackTxt` | varchar(50) | 是 |  | 否 |  | 黑名单内容，企业名称，统一社会编码，IP地址，Mac地址（瓯e保） |
| `blackType` | tinyint |  |  | 否 |  | 黑名单类型，0：统一社会编码，1：企业名称，2：IP地址，3：Mac地址（瓯e保） |

## T_Project_Info

*项目信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cProjectNo` | nvarchar(150) |  |  | 否 |  | 项目编号 |
| `cProjectType` | nvarchar(30) |  |  |  |  | 工程类型，如设计、施工等 |
| `cProjectName` | nvarchar(600) |  |  | 否 |  | 项目名称 |
| `cOwnerUnit` | nvarchar(100) |  |  |  |  | 业主单位名称 |
| `cOwnerUnitCode` | nvarchar(70) |  |  |  |  | 业主单位统一社会信用代码 |
| `fProjectAmount` | decimal(18,2) |  |  |  |  | 项目金额 |
| `fMarginAmountType` | tinyint |  |  | 否 | 0 | 保证金类型 0固定（默认） 1固定金额 2用户自定义 |
| `fMarginAmount` | decimal(18,2) |  |  |  |  | 保证金金额 |
| `cBidId` | varchar(150) |  |  |  |  | 标段ID |
| `cBidName` | nvarchar(600) |  |  |  |  | 标段名称 |
| `fBidTime` | datetime |  |  | 否 |  | 开标日期 |
| `cBiddingDocUrl` | nvarchar(3500) |  |  |  |  | 招标文件下载地址 |
| `cBiddingDocLocalUrl` | nvarchar(2000) |  |  |  |  | 招标文件本地地址 |
| `CreateTime` | datetime |  |  | 否 |  | 创建时间 |
| `tLatestUpTime` | datetime |  |  |  |  | 项目修改时间 |
| `DocUpdateTime` | datetime |  |  |  |  | 招标文件下载时间 |
| `cProUrl` | nvarchar(100) |  |  |  |  | 项目外部链接 |
| `fJoinCount` | int |  |  |  | 0 |  |
| `cProjectAddress` | nvarchar(100) |  |  |  |  |  |
| `cOwnerAddress` | nvarchar(100) |  |  |  |  |  |
| `cContactUserName` | nvarchar(30) |  |  |  |  |  |
| `cContactUserTel` | nvarchar(30) |  |  |  |  |  |
| `provinceName` | nvarchar(20) |  |  |  |  |  |
| `cityName` | nvarchar(20) |  |  |  |  |  |
| `areaName` | nvarchar(20) |  |  |  |  |  |
| `plannedDuration` | int |  |  |  | 0 |  |
| `managerId` | int |  |  | 否 | 0 |  |
| `fState` | tinyint |  |  | 否 | 0 | 0:正常，1:异常，2:草稿 |
| `PubTime` | datetime |  |  |  |  |  |
| `PRC_id` | int |  |  | 否 | 0 |  |
| `fEffectiveDay` | int |  |  |  |  |  |
| `tPayDepositDealineTime` | datetime |  |  |  |  |  |
| `cPublishUnit` | nvarchar(50) |  |  |  |  |  |
| `tPublishTime` | datetime |  |  |  |  |  |
| `bzjenddate` | datetime |  |  |  |  |  |
| `cApprovalCode` | nvarchar(150) |  |  |  |  |  |
| `cProjectCode` | nvarchar(100) |  |  |  |  |  |
| `cCityCode` | varchar(50) |  |  |  |  |  |
| `cOwnerBankCardNo` | varchar(50) |  |  |  |  |  |
| `cOwnerBank` | nvarchar(50) |  |  |  |  |  |
| `cOwnerAccount` | nvarchar(50) |  |  |  |  |  |
| `cBiddingNoticeUrl` | varchar(500) |  |  |  |  |  |
| `cTemplateType` | nvarchar(20) |  |  |  |  |  |
| `ExtendedJson` | nvarchar(MAX) |  |  |  |  |  |
| `cOwnerType` | tinyint |  |  | 否 | 1 |  |
| `cPerfProjectType` | nvarchar(4) |  |  |  |  |  |
| `cOwnerNature` | varchar(10) |  |  |  |  |  |
| `cOwnerSheng` | varchar(10) |  |  |  |  |  |
| `cOwnerShi` | varchar(10) |  |  |  |  |  |
| `cOwnerQu` | varchar(10) |  |  |  |  |  |
| `biaoduanstatus` | tinyint |  |  | 否 | 0 | 标段状态 0 正常 1 流标 2 终止 3 暂停 4 作废 |
| `fPrcPush` | tinyint |  |  | 否 | 0 | 推送 0默认 1已全部接收中心订单还原申请数据 2还原数据已全部推送中心 3还原文件已全部推送中心 |

## T_Epoint_PlatformConfig

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `platformname` | nvarchar(50) | 是 |  | 否 |  | 新点平台名称 |
| `unitname` | nvarchar(50) | 是 |  | 否 |  | 新点机构名称 |
| `cProvince` | nvarchar(50) |  |  | 否 |  | 省份 |
| `cCity` | nvarchar(50) |  |  | 否 |  | 城市 |
| `cArea` | nvarchar(50) |  |  | 否 |  | 县区 |
| `cOrgName` | nvarchar(50) |  |  | 否 |  | 机构名称 |
| `tdate` | datetime |  |  | 否 | getdate() |  |
| `startday` | date |  |  | 否 | '2000-1-1' |  |
| `endday` | date |  |  | 否 | '2099-12-31' |  |
| `newdate` | datetime |  |  | 否 | '2999-12-31' |  |
| `platformcode` | nvarchar(100) |  |  |  |  |  |
| `insurance_id` | int |  |  |  |  |  |
| `technology` | nvarchar(200) |  |  |  |  |  |
| `broker` | nchar |  |  |  |  | 经纪公司 |
| `isEncrypted` | bit |  |  |  |  | 是否加密 |
| `status` | int |  |  |  |  | 状态，待上线，已启用，已下线 |
| `remark` | nvarchar(MAX) |  |  |  |  |  |
| `fXKPlatformId` | tinyint |  |  | 否 | 0 | 线客平台id |

## T_GzZrx_PayLog

*雇主责任险--支付记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `transno` | varchar(50) | 是 |  | 否 |  | 银行流水号 |
| `transtime` | datetime |  |  | 否 |  | 支付时间 |
| `transamount` | decimal(18,2) |  |  | 否 |  | 支付金额 |
| `payeracctno` | varchar(50) |  |  | 否 |  | 付款卡号 |
| `payeracctname` | nvarchar(50) |  |  | 否 |  | 付款户名 |
| `abstractinfo` | nvarchar(50) |  |  |  |  | 银行备注 |
| `oppositebankno` | varchar(50) |  |  | 否 |  | 付款行号 |
| `oppositebankname` | nvarchar(50) |  |  | 否 |  | 付款行名 |
| `tdate` | datetime |  |  | 否 | getdate() | 日期 |
| `fState` | tinyint |  |  | 否 | 0 | 0:未使用，1：已使用，2：退款中，3：已退款 |
| `cardType` | tinyint |  |  | 否 | 0 | 付款卡归属，0：默认中银 |
| `skAccount` | varchar(50) |  |  | 否 | '' | 收款账号 |
| `cAuditUserName` | nvarchar(50) |  |  |  |  |  |
| `cAuditMessage` | nvarchar(100) |  |  |  |  |  |
| `cAuditTime` | datetime |  |  |  |  |  |
| `fIsTestPay` | tinyint |  |  | 否 | 0 | 0正式银行数据，1测试数据，2后台操作产生数据 |

## T_PProductYz_UserDataAccess

*数据权限角色*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `DataAccessName` | nvarchar(50) |  |  |  |  | 数据权限名称 |
| `Description` | nvarchar(200) |  |  |  |  | 用户组描述 |
| `Enabled` | bit |  |  |  | 1 | 是否启用 |
| `fUserCount` | int |  |  |  |  | 用户组人数 |
| `tCreateTime` | datetime |  |  |  |  | 创建时间 |
| `tUpdateTime` | datetime |  |  |  |  | 修改时间 |

## T_PRC_TypeModeSetting

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cLoginTypePic` | nvarchar(350) |  |  |  |  | 登录方式选项解释说明 |
| `cProjectTypePic` | nvarchar(350) |  |  |  |  | 项目信息选项解释说明 |
| `cPolicyholderPic` | nvarchar(350) |  |  |  |  | 投保人信息选项解释说明 |
| `cAccountInfoPic` | nvarchar(350) |  |  |  |  | 基本户信息选项解释说明 |
| `cSignTypePic` | nvarchar(350) |  |  |  |  | 签章模式选项解释说明 |
| `cServiceStylePic` | nvarchar(350) |  |  |  |  | 客服样式选项解释说明 |
| `cOrderClosePic` | nvarchar(350) |  |  |  |  | 订单关闭选项解释说明 |
| `tLastModifyDate` | datetime |  |  |  |  |  |
| `tCreateDate` | datetime |  |  |  | getdate() |  |

## T_ZX_UserLoginLog

*振鑫小程序用户登录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cOpenId` | varchar(100) |  |  |  |  | 微信OPENID |
| `tCreateTime` | datetime |  |  |  |  | 登录时间 |

## T_QuitGuarantee_AuditLogFile

*退保推送文件日志表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  |  |  | 关联订单表T_Guarantee_Info的cNewGuid |
| `cFileUrl` | varchar(200) |  |  |  |  | 文件地址 |
| `tCreateTime` | datetime |  |  |  | getdate() |  |

## T_QuitGuarantee_PRCEnInsuranceEnAttachment

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCEnInsuranceID` | int |  |  | 否 |  |  |
| `fAttachmentID` | int |  |  | 否 |  |  |
| `fIsRequired` | tinyint |  |  | 否 | 0 |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |
| `fIsShow` | tinyint |  |  | 否 | 0 | 是否显示 0 否 1 是 |
| `cAttachDesc` | nvarchar(50) |  |  |  |  | 附件话术 |

## T_PProduct_IntegratedPRC

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fIntegratedPRCid` | int |  |  |  |  | T_PProduct_IntegratedPRC表ID |
| `fAttachmentID` | int |  |  |  |  | T_PProduct_Enclosure表ID |
| `cAttachmentName` | varchar(200) |  |  |  |  | 附件名称 |
| `cAttachmentCode` | varchar(150) |  |  |  |  | 附件编码 |
| `fIsUpLoad` | tinyint |  |  |  |  | 是否上传 |
| `fIsRequired` | tinyint |  |  |  |  | 是否必填 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cLastEditUser` | nvarchar(50) |  |  |  |  | 最后修改人 |
| `tLastEditTime` | datetime |  |  |  |  | 最后修改时间 |
| `fFlieType` | tinyint |  |  |  |  | 文件类型 1图片 2其他 |
| `cFileTempUrl` | varchar(200) |  |  |  |  |  |
| `cDisplayName` | nvarchar(100) |  |  |  |  |  |
| `cDesc` | nvarchar(100) |  |  |  |  |  |
| `fSort` | int |  |  |  |  |  |

## T_Enterprise_Attachment

*企业附件表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `cName` | nvarchar(100) |  |  |  |  | 附件文件名称 |
| `cUrl` | varchar(1000) |  |  |  |  | 附件地址 |
| `CreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `fIsDelete` | bit |  |  | 否 | 0 | 是否删除（0否，1是 |
| `fPid` | int |  |  | 否 | 0 |  |
| `fSid` | int |  |  | 否 | 0 |  |
| `cLocalUrl` | varchar(800) |  |  |  |  |  |
| `FileMD5` | varchar(40) |  |  |  |  |  |

## T_Login_Log

*登陆日志表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  | 否 |  | 企业表ID |
| `cIP` | varchar(50) |  |  | 否 |  | IP地址 |
| `tdate` | datetime |  |  | 否 | getdate() | 登陆时间 |

## T_PProductYz_UserDataAccess_Coinsurant

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `DataAccessID` | int |  |  |  |  | T_PProductYz_UserDataAccess表ID |
| `CoinsurantID` | int |  |  |  |  | T_PProductYz_Coinsurant表ID |
| `tCreateTime` | datetime |  |  |  |  | 创建时间 |
| `cCoinsurantName` | nvarchar(50) |  |  |  |  | 共保体名称 |
| `cSheng` | nvarchar(50) |  |  |  |  | 省 |
| `cShi` | nvarchar(50) |  |  |  |  | 市 |
| `cQu` | nvarchar(50) |  |  |  |  | 区 |
| `cPlatformProvinceCode` | nvarchar(50) |  |  |  |  | 省编码 |
| `cPlatformCityCode` | nvarchar(50) |  |  |  |  | 市编码 |
| `cPlatformCountyCode` | nvarchar(50) |  |  |  |  | 区编码 |

## T_PProduct_IntegratedProduct

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cFullName` | nvarchar(50) |  |  |  |  | 产品名称 |
| `cCode` | nvarchar(50) |  |  |  |  | 产品编码 |
| `cShortName` | nvarchar(50) |  |  |  |  | 产品简称 |
| `cAbout` | text |  |  |  |  | 产品说明 |
| `cPicUrl` | nvarchar(200) |  |  |  |  | 产品配图 |
| `cRemark` | nvarchar(500) |  |  |  |  | 备注 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cProcessedIconUrl` | nvarchar(200) |  |  |  |  | 已办理图标 |
| `cUnProcessedIconUrl` | nvarchar(200) |  |  |  |  | 未办理图标 |

## T_ZX_GoodsImg

*振鑫小程序-商品信息详情图表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fGoodsID` | int |  |  |  | 0 | 商品ID，关联T_ZX_GoodsInfo商品表ID |
| `cPic` | varchar(50) |  |  |  |  | 图片地址 |

## T_MobileMsg_Blacklist

*短信黑名单*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cTel` | varchar(50) |  |  |  |  | 手机号 |
| `CreateTime` | datetime |  |  |  |  |  |

## T_XK_RebateDetail_Apply

*返点退回申请*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fDetailId` | int |  |  |  |  |  |
| `cReturnUrl` | nvarchar(350) |  |  |  |  | 标记已退附件 |
| `cReturnDesc` | nvarchar(200) |  |  |  |  | 标记已退--备注 |
| `fReturnStatus` | tinyint |  |  |  | 0 | 标记已退状态（0：未标记；1：已标记） |
| `cReturnUser` | nvarchar(50) |  |  |  | (0) | 标记已退申请人 |
| `tReturnTime` | datetime |  |  |  |  | 申请时间（标记已退时间） |
| `fReturnAuthStatus` | tinyint |  |  |  | 0 | 标记已退审核结果（0：待处理；1：审核通过；2：审核驳回） |
| `cReturnAuthUser` | nvarchar(50) |  |  |  | (0) | 标记已退审核人 |
| `cReturnAuthDesc` | nvarchar(200) |  |  |  |  | 标记已退审核意见 |
| `tReturnAuthTime` | datetime |  |  |  |  | 标记已退-审核时间 |

## T_PProductYz_UserDataAccess_Organ

*数据权限角色详情*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `DataAccessID` | int |  |  |  |  | T_PProductYz_UserDataAccess表ID |
| `OrganID` | int |  |  |  |  | T_PProductYz_Organ表ID |
| `cOrganName` | nvarchar(50) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cSheng` | nvarchar(50) |  |  |  |  | 省 |
| `cShi` | nvarchar(50) |  |  |  |  | 市 |
| `cQu` | nvarchar(50) |  |  |  |  | 区 |
| `cPlatformProvinceCode` | nvarchar(50) |  |  |  |  | 省编码 |
| `cPlatformCityCode` | nvarchar(50) |  |  |  |  | 市编码 |
| `cPlatformCountyCode` | nvarchar(50) |  |  |  |  | 区编码 |

## T_PProduct_IntegratedRule

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fCommodityID` | int |  |  |  |  | 关联商品 |
| `fSGContractAmountMin` | decimal(18,2) |  |  |  |  | 施工合同金额最小值(元) |
| `fSGContractAmountMax` | decimal(18,2) |  |  |  |  | 施工合同金额最大值(元) |
| `fSGContractAmountType` | tinyint |  |  |  |  | 施工合同金额范围类型 1左开右闭 2左闭右开 |
| `fRate` | decimal(18,4) |  |  |  |  | 费率 |
| `fMarginAmountMax` | decimal(18,2) |  |  |  |  | 最高保证金金额(元) |

## T_ZX_EquityCouponGroupEnCoupon

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEquityCouponGroupID` | int |  |  | 否 | 0 | 权益优惠券组T_ZX_EquityCouponGroup表id |
| `fCouponTypeID` | int |  |  | 否 | 0 | 优惠券T_Coupon_Type表id |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |
| `fCount` | int |  |  | 否 | 1 | 优惠券发数量 |

## T_MobileMsg_Log

*短信发送日志*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  | 企业表ID |
| `cTel` | varchar(50) |  |  |  |  | 手机号 |
| `cCode` | varchar(10) |  |  |  |  | 码 |
| `cContent` | nvarchar(500) |  |  |  |  | 短信内容 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |
| `cErrorMsg` | nvarchar(50) |  |  |  |  | 返回错误提示 |
| `fFrom` | tinyint |  |  |  | 0 | 1凭证上传提醒客服，2后台登录验证码，9天安绑定手机号，10天安找回忘记密码 , 130：新点渠道 |
| `cSMSid` | nvarchar(10) |  |  |  |  |  |

## T_Epoint_Guarantee

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `applyno` | varchar(50) | 是 |  | 否 |  | 保函编号 |
| `platformname` | nvarchar(50) |  |  | 否 |  | 平台名称 |
| `unitname` | nvarchar(50) |  |  | 否 |  | 出函机构 |
| `danweiname` | nvarchar(200) |  |  | 否 |  | 投标企业单位名称 |
| `orgnum` | varchar(200) |  |  | 否 |  | 投标人信用代码 |
| `contactperson` | nvarchar(200) |  |  | 否 |  | 投标单位联系人 |
| `contactphone` | varchar(200) |  |  | 否 |  | 投标单位联系方式 |
| `baofei` | decimal(18,2) |  |  | 否 |  | 保费金额 |
| `bzjamount` | decimal(18,2) |  |  | 否 |  | 保证金金额 |
| `successdate` | datetime |  |  |  |  | 出函时间 |
| `kaibiaotime` | datetime |  |  | 否 |  | 开标时间 |
| `biaoduanno` | varchar(200) |  |  | 否 |  | 标段编号 |
| `biaoduanname` | nvarchar(200) |  |  | 否 |  | 标段名称 |
| `zbr` | nvarchar(200) |  |  | 否 |  | 招标人 |
| `zbrorgnum` | nvarchar(200) |  |  | 否 |  | 招标人统一社会信用代码 |
| `tdate` | datetime |  |  | 否 | getdate() | 入库时间 |
| `baohanno` | varchar(50) |  |  |  |  |  |
| `referralcode` | nvarchar(50) |  |  |  |  |  |
| `issuccess` | nvarchar(10) |  |  | 否 | '' |  |

## T_PRC_InterfaceLimit

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `platformcode` | varchar(50) |  |  | 否 |  | 平台编码 |
| `cInsuranceCompany` | nvarchar(50) |  |  |  |  | 机构简称 |
| `message` | nvarchar(200) |  |  |  |  | 返回信息 |
| `fState` | tinyint |  |  | 否 | 0 | 0 未生效 1 生效 |
| `tdate` | datetime |  |  | 否 | getdate() | 创建时间 |

## T_PProductYz_UserDataAccess_PRC

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `DataAccessID` | int |  |  | 否 |  | T_PProductYz_UserDataAccess表ID |
| `PrcId` | int |  |  | 否 |  | T_PProductYz_RPC表ID |
| `cPRCCode` | nvarchar(50) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cPRCName` | nvarchar(50) |  |  |  |  | 渠道名称 |
| `cSheng` | nvarchar(50) |  |  |  |  | 省 |
| `cShi` | nvarchar(50) |  |  |  |  | 市 |
| `cQu` | nvarchar(50) |  |  |  |  | 区 |
| `cPlatformProvinceCode` | nvarchar(50) |  |  |  |  | 省编码 |
| `cPlatformCityCode` | nvarchar(50) |  |  |  |  | 市编码 |
| `cPlatformCountyCode` | nvarchar(50) |  |  |  |  | 区编码 |

## T_PProduct_InvoiceInfo

*履约企业发票信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `fType` | tinyint |  |  |  | 0 |  |
| `cUser` | nvarchar(20) |  |  |  |  |  |
| `cUserPhone` | varchar(50) |  |  |  |  |  |
| `cAddress` | nvarchar(50) |  |  |  |  |  |
| `cEmail` | nvarchar(40) |  |  |  |  |  |
| `cTel` | varchar(50) |  |  |  |  |  |
| `cBank` | nvarchar(30) |  |  |  |  |  |
| `cAccount` | nvarchar(30) |  |  |  |  |  |
| `CreateTime` | datetime |  |  |  | getdate() |  |
| `cCompanyAddress` | nvarchar(100) |  |  |  |  |  |
| `SignInvoice` | varchar(200) |  |  | 否 | '' |  |
| `isSignInvoice` | tinyint |  |  | 否 | 0 |  |
| `cTaxPayerNo` | varchar(50) |  |  |  |  |  |
| `cTaxPayerFile` | varchar(200) |  |  |  |  | 纳税证明文件 |

## T_Esign_ApplyDetail

*签章文件列表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fApplyId` | int |  |  |  |  | T_Esign_Apply 表ID |
| `tCreateDate` | datetime |  |  |  |  |  |
| `cFileUrl` | nvarchar(500) |  |  |  |  | 签章前文件 |
| `cSignFileUrl` | nvarchar(500) |  |  |  |  | 签章后文件(过程文件，有3个章要盖，目前只盖了第一个，这边就存第一个盖章后的文件。) |
| `fIsDelete` | tinyint |  |  | 否 | 0 |  |

## T_MobileMsg_Tel

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cTag` | varchar(20) |  |  | 否 |  | 标签名称 |
| `cTel` | varchar(11) |  |  | 否 |  | 手机号 |
| `CreateTime` | datetime |  |  | 否 | getdate() |  |
| `cRemark` | nvarchar(50) |  |  |  |  | 备注 |
| `ID` | int | 是 | 是 | 否 |  |  |

## T_GzZrx_PaymentVouchers

*雇主责任险-上传凭证记录*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fGuaranteeInfoID` | int |  |  |  | 0 | 保单表ID |
| `cPaymentNo` | nvarchar(100) |  |  |  |  | 上传凭证序列号 |
| `cPaymentUrl` | nvarchar(100) |  |  |  |  | 凭证上传地址 |
| `CreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `fIsSend` | tinyint |  |  |  | 0 |  |
| `cAuditMessage` | nvarchar(50) |  |  |  |  |  |
| `cAuditUserName` | nvarchar(50) |  |  |  |  |  |
| `cAuditTime` | datetime |  |  |  |  |  |

## T_ZX_ConstructionGrade

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 |  | 否 |  |  |
| `cConstructionGrade` | nvarchar(10) |  |  |  |  |  |

## T_PProductYz_UserRoles

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Id` | int | 是 | 是 | 否 |  |  |
| `CreateDateTime` | datetime2 |  |  | 否 |  | 创建时间 |
| `IsDeleted` | bit |  |  | 否 |  | 是否删除 |
| `RoleId` | int |  |  | 否 |  | T_PProductYz_Roles表ID |
| `UserId` | int |  |  | 否 |  | T_PProductYz_Users表ID |

## T_Guarantee_Project

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `PRC_id` | int |  |  |  |  | T_PRC_Info表id |
| `Insurance_id` | int |  |  |  |  | T_Insurance_Info表id |
| `provinceName` | nvarchar(20) |  |  |  |  | 省 |
| `cityName` | nvarchar(20) |  |  |  |  | 市 |
| `areaName` | nvarchar(20) |  |  |  |  | 区 |
| `prcInsuranceName` | nvarchar(50) |  |  |  |  | 保险公司名 |
| `projectName` | nvarchar(450) |  |  |  |  | 项目名称 |
| `bidFileCode` | nvarchar(300) |  |  |  |  | 招标文件编号 |
| `bidFileUrls` | varchar(MAX) |  |  |  |  | 招标文件地址，逗号隔开 |
| `fProjectAmount` | decimal(18,2) |  |  |  |  | 项目造价（万） |
| `fMarginAmount` | decimal(18,2) |  |  |  |  | 保证金额（万） |
| `PlannedDuration` | int |  |  |  |  | 计划工期(天) |
| `fBidTime` | datetime |  |  |  |  | 开标时间 |
| `cProjectAddress` | nvarchar(100) |  |  |  |  | 项目地址 |
| `cTenderCompanyName` | nvarchar(50) |  |  |  |  | 招标单位名称 |
| `cTenderCreditcode` | varchar(50) |  |  |  |  | 招标单位统一社会信用代码 |
| `cTenderContact` | nvarchar(30) |  |  |  |  | 招标单位联系人 |
| `cContactTel` | nvarchar(50) |  |  |  |  | 单位联系电话 |
| `cTenderCompanyAddr` | nvarchar(100) |  |  |  |  | 单位地址 |
| `rProjectId` | int |  |  |  |  | 关联项目Id（如果有） |
| `CreateTime` | datetime |  |  | 否 |  | 创建时间 |
| `cOwnerNature` | varchar(10) |  |  |  |  |  |
| `cOwnerSheng` | varchar(10) |  |  |  |  |  |
| `cOwnerShi` | varchar(10) |  |  |  |  |  |
| `cOwnerQu` | varchar(10) |  |  |  |  |  |
| `cProjectType` | nvarchar(30) |  |  |  |  |  |
| `fMarginAmountType` | tinyint |  |  | 否 | 0 |  |
| `cProjectNo` | nvarchar(150) |  |  |  |  |  |
| `cProjectName` | nvarchar(200) |  |  |  |  |  |
| `cBidId` | nvarchar(150) |  |  |  |  |  |
| `cBidName` | nvarchar(200) |  |  |  |  |  |

## T_PProduct_Enterprise

*农民工履约企业表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  | 否 |  | 企业表id |
| `cName` | nvarchar(50) |  |  |  |  | 姓名 |
| `cMobile` | varchar(50) |  |  |  |  | 手机号 |
| `cPwd` | varchar(100) |  |  |  |  | 密码 |
| `cPosition` | nvarchar(50) |  |  |  |  | 岗位 |
| `cDesc` | nvarchar(300) |  |  |  |  | 备注 |
| `tCreateTime` | datetime |  |  |  |  | 创建日期 |
| `fState` | tinyint |  |  | 否 | 1 | 状态（0：停用；1：启用） |

## T_Esign_ApplyDetail_Signs

*签章步骤*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fApplyId` | int |  |  |  |  | T_Esign_Apply 表ID |
| `fApplyDetailId` | int |  |  |  |  | T_Esign_ApplyDetail 表id |
| `cOwner` | nvarchar(50) |  |  |  |  | 主体 |
| `fType` | tinyint |  |  |  |  | 印章类型（1：合同专用章 2：财务章；3：法人章；4：公章；5：业务结算章） |
| `cPages` | nvarchar(50) |  |  |  |  | 签章页面 |
| `cKey` | nvarchar(50) |  |  |  |  | 关键字签章定位 |
| `fIsQF` | tinyint |  |  |  | 0 | 是否骑缝章（0：否；1：是） |
| `tCreateDate` | datetime |  |  |  |  |  |
| `cSignFileUrl` | nvarchar(500) |  |  |  |  | 签章后文件 |
| `fIsSigned` | tinyint |  |  |  | 0 | 是否已签章（0：否；1：是） |
| `fSort` | int |  |  |  |  | 排序 |
| `tSignTime` | datetime |  |  |  |  | 最后一次调用签章接口时间 |
| `fQFPages` | int |  |  | 否 | 0 | 骑缝章盖章页码 |
| `cQFLocation` | nvarchar(10) |  |  |  |  | 骑缝章位置 |
| `fIsDelete` | tinyint |  |  | 否 | 0 |  |

## T_News_Cla

*新闻帮助类别表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cClaName` | nvarchar(50) |  |  |  |  | 类别名称 |
| `fPid` | int |  |  |  | 0 | 上级类别id |
| `cPath` | varchar(50) |  |  |  |  | 类别路径 |
| `fLevl` | int |  |  |  | 0 | 类别级别 |
| `fOrder` | int |  |  |  | 0 | 排序 |
| `fDisplay` | bit |  |  |  | 0 | 是否显示 |
| `CreateTime` | datetime |  |  |  |  |  |

## T_Epoint_PushGuarantee

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `GuaranteeId` | int |  |  |  |  | T_Epoint_PushGuarantee表ID |
| `Operator` | nvarchar(50) |  |  |  |  | 操作人 |
| `OperationTime` | datetime |  |  |  |  | 操作时间 |
| `OperationType` | nvarchar(50) |  |  |  |  | 操作类型 |
| `OperationLog` | nvarchar(MAX) |  |  |  |  | 历史数据（操作记录） |
| `ImportId` | int |  |  |  |  | 导入记录表ID |

## T_PProductYz_Users

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Id` | int | 是 | 是 | 否 |  |  |
| `tCreateTime` | datetime |  |  | 否 |  |  |
| `Email` | nvarchar(36) |  |  |  |  |  |
| `IsDeleted` | bit |  |  | 否 |  |  |
| `IsSuperMan` | bit |  |  | 否 |  |  |
| `LoginName` | nvarchar(20) |  |  | 否 |  |  |
| `Password` | nvarchar(50) |  |  | 否 |  |  |
| `RealName` | nvarchar(20) |  |  | 否 |  |  |
| `IsDisable` | bit |  |  | 否 | 0 |  |
| `TelePhone` | varchar(50) |  |  | 否 |  |  |
| `LastLoginCount` | int |  |  | 否 | 0 | 登录错误次数 |
| `LastLoginTime` | datetime |  |  |  |  | 上次登录时间 |
| `updatePWDTime` | datetime |  |  |  |  | 密码修改时间 |
| `DataAccess` | int |  |  |  |  | 数据权限 |
| `InsuranceInfoId` | int |  |  |  |  | T_PProduct_InsuranceInfo表ID，保司账号所属保司 |
| `fUserType` | tinyint |  |  |  | 0 | 账号类型：0：其他 1：保司 2: 医院 3: 医调委 |
| `cRemark` | nvarchar(200) |  |  |  |  | 备注 |
| `cCompanyName` | nvarchar(100) |  |  |  |  |  |

## T_PProduct_Log

*农民工操作日志表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fProjectID` | int |  |  |  | 0 | 项目表ID |
| `fGuaranteeID` | int |  |  |  | 0 | 保单表ID |
| `CreateTime` | datetime |  |  |  |  |  |
| `cDes` | nvarchar(350) |  |  |  |  |  |
| `cUserID` | varchar(50) |  |  |  |  | 录入的用户ID，对应T_PProduct_Admin表ID |

## T_Host_Redirect

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `host` | varchar(100) | 是 |  | 否 |  | 原始地址 |
| `redirect` | varchar(100) |  |  | 否 |  | 目标地址 |
| `tdate` | datetime |  |  | 否 | getdate() |  |
| `schemeOld` | varchar(50) |  |  |  |  |  |
| `schemeNew` | varchar(50) |  |  |  |  |  |
| `remarks` | nvarchar(50) |  |  |  |  | 备注 |
| `logkey` | varchar(50) |  |  |  |  |  |

## T_News_Info

*新闻帮助信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fCla` | int |  |  |  | 0 | 类别ID |
| `cTitle` | nvarchar(50) |  |  |  |  | 标题 |
| `cPic` | varchar(200) |  |  |  |  | 图片地址 |
| `cKey` | nvarchar(50) |  |  |  |  | 关键词 |
| `cAbout` | nvarchar(50) |  |  |  |  | 关于 |
| `cContent` | nvarchar(MAX) |  |  |  |  | 内容 |
| `cUrl` | varchar(200) |  |  |  |  | 外链接 |
| `cAuthor` | nvarchar(20) |  |  |  |  | 作者 |
| `fTopping` | int |  |  |  | 0 | 置顶值 |
| `CreateTime` | datetime |  |  |  |  |  |
| `fIsDelete` | bit |  |  |  | 0 |  |
| `cFrom` | nvarchar(200) |  |  |  |  |  |

## T_PProduct_PushTimeLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  |  |  | 订单编号，对应订单表 |
| `cName` | nvarchar(70) |  |  |  |  | 推送事件名称 |
| `tCreateTime` | datetime |  |  |  | getdate() | 事件发生时间 |
| `cInfo` | nvarchar(300) |  |  |  |  | 提示信息 |
| `fType` | tinyint |  |  | 否 | 0 |  |
| `cPostJson` | varchar(MAX) |  |  |  |  |  |
| `cResultJsonData` | varchar(MAX) |  |  |  |  |  |

## T_PProduct_Manual

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  |  |  |  |
| `cPolicyNo` | nvarchar(50) |  |  |  |  |  |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  |  |
| `cRealName` | nvarchar(50) |  |  |  |  |  |
| `cPhone` | nvarchar(50) |  |  |  |  |  |
| `tPolicyTime` | datetime |  |  |  |  |  |
| `tQuitApplyTime` | datetime |  |  | 否 | getdate() |  |
| `fState` | int |  |  | 否 | 0 |  |
| `quitIsPush` | int |  |  | 否 | 0 |  |
| `fQuitState` | tinyint |  |  | 否 | 0 |  |
| `cAuditUserName` | nvarchar(50) |  |  |  |  |  |
| `cReason` | nvarchar(200) |  |  |  |  |  |
| `cFileUrls` | varchar(200) |  |  |  |  |  |
| `platformcode` | varchar(50) |  |  |  |  |  |
| `fPayId` | int |  |  |  |  |  |
| `fIsTest` | tinyint |  |  | 否 | 0 | 是否测试数据 |
| `Prc_Type` | tinyint |  |  | 否 | 0 | 平台类型：0新点，1擎州，2温州、平阳 |
| `cRemark` | nvarchar(100) |  |  |  |  |  |
| `cLicenseLocalUrl` | varchar(100) |  |  |  |  |  |
| `cAccountCertLocalUrl` | varchar(100) |  |  |  |  |  |
| `cBiddingDocLocalUrl` | varchar(100) |  |  |  |  |  |
| `cCorporationIDCardLocalUrl` | varchar(100) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |
| `cToQuitEsignUrl` | varchar(200) |  |  |  |  |  |
| `cQuitEsignUrl` | varchar(200) |  |  |  |  |  |
| `cToQuitAccountEsignUrl` | varchar(200) |  |  |  |  |  |
| `cQuitAccountEsignUrl` | varchar(200) |  |  |  |  |  |
| `tQuitEsignTime` | datetime |  |  |  |  |  |
| `tQuitFinishTime` | datetime |  |  |  |  |  |
| `fQuitFrom` | tinyint |  |  | 否 | 2 | 1 接口推送 2 手动添加 3 退保2.0 |

## T_Epoint_BaseAccountLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cNewGuid` | varchar(50) | 是 |  | 否 |  |  |
| `cBaseAccountUrl` | varchar(200) |  |  |  |  |  |
| `tDate` | datetime |  |  | 否 | getdate() |  |

## T_OFD_Interface

*OFD接口配置表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `PRC_id` | int | 是 |  | 否 |  |  |
| `Insurance_id` | int | 是 |  | 否 |  |  |
| `ServerIP` | varchar(50) |  |  | 否 |  | OFD接口IP |
| `ServerPort` | int |  |  | 否 |  | OFD接口端口号 |
| `TemplateName` | nvarchar(50) |  |  | 否 |  | OFD报文模版名称 |
| `tdate` | datetime |  |  | 否 | getdate() |  |
| `decryptServerIP` | varchar(50) |  |  |  |  | 明文接口IP |
| `decryptPort` | int |  |  |  |  | 明文接口端口号 |
| `keyCD` | varchar(50) |  |  |  |  | 益高-密文-流程标识 |
| `keyPD` | varchar(50) |  |  |  |  | 益高-明文-流程标识 |
| `identificationCD` | varchar(50) |  |  |  |  | 单证识别码-密文 |
| `identificationPD` | varchar(50) |  |  |  |  | 单证识别码-明文 |
| `sealId` | varchar(50) |  |  |  |  | 章模ID |
| `callSystem` | varchar(50) |  |  |  |  | 调用系统标识 |

## T_Esign_SignRecord

*签章记录*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fApplyId` | int |  |  |  |  | T_Esign_Apply 表id |
| `fApplyDetailId` | int |  |  |  |  | T_Esign_ApplyDetail 表id |
| `cFileUrl` | nvarchar(500) |  |  |  |  | 签章前文件 |
| `cSignFileUrl` | nvarchar(500) |  |  |  |  | 签章后文件 |
| `tCreateDate` | datetime |  |  |  | getdate() |  |
| `cAuthUser` | nvarchar(50) |  |  |  |  |  |
| `cAuthUserId` | nvarchar(100) |  |  |  |  |  |
| `fFrom` | tinyint |  |  | 否 | 0 | 来源（0：内部电子用章；1：国科） |

## T_PaymentSystem_PlatformBusiness

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cNumber` | varchar(50) | 是 |  | 否 |  | 业务平台编号 |
| `cPlatformNumber` | varchar(50) |  |  |  |  | 主平台编号 |
| `cInsuranceNumber` | varchar(50) |  |  |  |  | 保险公司编号 |
| `cOrgName` | nvarchar(50) |  |  |  |  | 承保机构名称 |
| `cBank` | nvarchar(50) |  |  |  |  | 收款开户行 |
| `cUserName` | nvarchar(50) |  |  |  |  | 收款账户名称 |
| `cAccount` | varchar(50) |  |  |  |  | 收款账号 |
| `cRemarks` | nvarchar(100) |  |  |  |  | 备注 |
| `cProvince` | nvarchar(30) |  |  |  |  | 省 |
| `cCity` | nvarchar(30) |  |  |  |  | 市 |
| `cArea` | nvarchar(30) |  |  |  |  | 区 |
| `CreateTime` | datetime |  |  |  | getdate() |  |
| `pushUrl` | varchar(200) |  |  |  |  |  |
| `payPage` | varchar(200) |  |  |  |  |  |
| `MinfPremium` | decimal(10,2) |  |  |  |  |  |
| `fRate` | decimal(10,2) |  |  |  |  |  |
| `dataapiurl` | varchar(200) |  |  |  |  |  |
| `cBlackCheckUrl` | varchar(200) |  |  |  |  |  |
| `cLocalBlackCheckUrl` | nvarchar(200) |  |  |  |  | 内部平台黑名单验证接口 |
| `fIsRecipient` | tinyint |  |  | 否 | 1 | 是否中惠代收（1：是；0：否）  这个参数会影响【退款事项处理】功能流程 |
| `fIsPushErrorState` | tinyint |  |  | 否 | 0 |  |
| `fXKPlatformId` | int |  |  | 否 | 0 |  |
| `fRunState` | tinyint |  |  |  | 0 |  |
| `id` | int |  | 是 | 否 |  |  |
| `cMaualCity` | nvarchar(50) |  |  |  |  |  |
| `cMaualArea` | nvarchar(50) |  |  |  |  |  |

## T_ZX_PointsInfo

*担保小程序-积分记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPointsUserID` | int |  |  |  | 0 | 关联T_ZX_PointsUser表ID |
| `fZXUserID` | int |  |  |  | 0 | 关联T_ZX_User表ID |
| `cTitle` | nvarchar(30) |  |  |  |  | 标题 |
| `fPoints` | int |  |  |  | 0 | 积分 |
| `fZt` | tinyint |  |  |  | 0 | 积分状态，默认0无效，1增加，2减去 |
| `fNewPoints` | int |  |  |  | 0 | 最新用户积分 |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `cNewGuid` | varchar(50) |  |  |  |  | 关联T_ZX_GoodsRecord表cNewGuid |

## T_GzZrx_Insurance

*雇主责任险-险种表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cInsuranceCode` | varchar(20) |  |  | 否 |  | 金融机构编码 |
| `cInsuranceName` | nvarchar(20) |  |  | 否 |  | 金融机构名称 |
| `cInsuranceFullName` | nvarchar(50) |  |  |  |  | 金融机构全称 |
| `fInsuranceType` | tinyint |  |  | 否 | 0 | 金融机构类型 0 保险公司 1 银行 2 担保公司 |
| `cInsuranceLogo` | varchar(100) |  |  |  |  | 金融机构logo |
| `cOrderLogo` | varchar(100) |  |  |  |  | 订单logo |
| `cInvoiceTitle` | nvarchar(100) |  |  |  |  | 发票申请窗口名称 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |

## T_PRC_TypeMode

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cLoginTypePic` | nvarchar(350) |  |  |  |  | 登录方式选项解释说明 |
| `cProjectTypePic` | nvarchar(350) |  |  |  |  | 项目信息选项解释说明 |
| `cPolicyholderPic` | nvarchar(350) |  |  |  |  | 投保人信息选项解释说明 |
| `cAccountInfoPic` | nvarchar(350) |  |  |  |  | 基本户信息选项解释说明 |
| `cSignTypePic` | nvarchar(350) |  |  |  |  | 签章模式选项解释说明 |
| `cServiceStylePic` | nvarchar(350) |  |  |  |  | 客服样式选项解释说明 |
| `cOrderClosePic` | nvarchar(350) |  |  |  |  | 订单关闭选项解释说明 |
| `tLastModifyDate` | datetime |  |  |  |  |  |
| `tCreateDate` | datetime |  |  |  | getdate() |  |

## T_PProduct_OfflineInsuranceInfo

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cInsuranceName` | nvarchar(10) |  |  | 否 |  | 机构简称 |
| `cInsuranceFullName` | nvarchar(20) |  |  | 否 |  | 机构全称 |
| `tdate` | datetime |  |  | 否 | getdate() | 创建时间 |
| `cInvoiceTitle` | varchar(200) |  |  |  |  | 发票弹窗标题名称 |
| `fInsuranceType` | tinyint |  |  | 否 | 0 | 金融机构类型 |
| `fInsuranceCode` | nvarchar(50) |  |  |  |  | 金融机构编码 |

## T_Offline_Manager

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cPartnersNum` | varchar(50) |  |  | 否 |  | 合作方编号 |
| `cPartnersShortName` | nvarchar(50) |  |  |  |  | 合作方简称 |
| `cPartnersFullName` | nvarchar(50) |  |  |  |  | 合作方全称 |
| `cSheng` | nvarchar(30) |  |  |  |  |  |
| `cShi` | nvarchar(30) |  |  |  |  |  |
| `cQu` | nvarchar(30) |  |  |  |  |  |
| `cAptitudePicture` | varchar(MAX) |  |  |  |  | 资质图片，多图片以,隔开 |
| `cUserName` | varchar(50) |  |  |  |  | 管理员账号 |
| `cUserTel` | varchar(20) |  |  |  |  | 管理员手机号 |
| `cUserPwd` | varchar(50) |  |  |  |  | 管理员密码 |
| `cRemarks` | nvarchar(50) |  |  |  |  | 备注 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |
| `fLoginErrCount` | int |  |  |  |  | 登录错误次数 |
| `tLoginTime` | datetime |  |  |  |  | 登陆时间 |
| `fState` | tinyint |  |  |  | 0 | 状态：0禁用，1启用 |
| `cEnterpriseNameCode` | varchar(50) |  |  |  |  |  |
| `cPermission` | varchar(50) |  |  |  |  |  |
| `fAreaDataPermission` | tinyint |  |  | 否 | 1 |  |
| `fBidDataPermission` | tinyint |  |  | 否 | 1 |  |
| `AuthPhone` | varchar(500) |  |  |  |  | 授权登录手机号 |
| `SysType` | tinyint |  |  | 否 | 0 |  |
| `MgrType` | tinyint |  |  | 否 | 0 |  |
| `RelPlatformcodes` | varchar(500) |  |  |  |  |  |
| `cDataServicePhone` | varchar(500) |  |  |  |  |  |

## T_XK_Contacts_DataStatisticsExtend

*线客联系人出单数据监测预警状态表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `fDataStatisticsID` | int | 是 |  | 否 |  | 关联T_XK_Contacts_DataStatistics表ID |
| `cWarningStatus` | varchar(10) |  |  |  | (0) | 预警状态 |

## T_Relation_PRCEnInsurance

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `fPRCEnInsuranceID` | int | 是 |  | 否 | 0 | 对应T_Relation_PRCEnInsurance表ID |
| `userAcct` | varchar(30) |  |  |  |  | 配置账号 |
| `password` | varchar(30) |  |  |  |  | 配置密码 |
| `productCode` | varchar(30) |  |  |  |  | 易联方案代码 |
| `programCode` | varchar(30) |  |  |  |  | 易联对接编号 |
| `projectCode` | varchar(30) |  |  |  |  | 易联项目编码 |
| `invoice_merchantNo` | varchar(30) |  |  |  |  | 商户号(请求来源） |
| `invoice_qudao` | varchar(30) |  |  |  |  | 发票渠道标识 |
| `invoice_md5Salt` | varchar(30) |  |  |  |  | 发票md5加盐 |
| `pigai_loginName` | varchar(30) |  |  |  |  | 批改登录名 |
| `pigai_jointBusinessCode` | varchar(30) |  |  |  |  | 批改渠道来源 |
| `pigai_actual_productCode` | varchar(30) |  |  |  |  | 批改险种代码 |
| `fState` | tinyint |  |  |  | 0 | 状态，0禁用，1启用 |
| `yewulaiyuan` | varchar(30) |  |  |  |  | 业务来源 |
| `chudanyuan` | varchar(30) |  |  |  |  | 出单员代码 |
| `zhidanjigou` | varchar(30) |  |  |  |  | 制单机构（出单员归属机构） |
| `yewuyuan` | varchar(30) |  |  |  |  | 业务员代码 |
| `yewuyuanjigou` | varchar(30) |  |  |  |  | 业务归属机构代码（业务员的归属机构） |
| `hebaoyuan` | varchar(30) |  |  |  |  | 核保员代码 |
| `dailiren` | varchar(30) |  |  |  |  | 代理人代码 |
| `dailirenxieyi` | varchar(30) |  |  |  |  | 代理人协议号 |
| `shouxvfei` | varchar(10) |  |  |  | (0) | 手续费比例 |
| `yingxiaoqudao` | varchar(30) |  |  |  |  | 营销渠道 |
| `qixian` | varchar(10) |  |  |  |  | 保险期限（单位：月） |
| `danzhengleixing` | varchar(10) |  |  |  |  | 单证类型（凭证类型），100表示不输出凭证 |
| `zhugongbao` | tinyint |  |  |  | 0 | 是否主共保，默认0否，1是 |
| `ofd` | tinyint |  |  |  | 0 | 是否OFD，默认0否，1是 |
| `invoice_downApiUrl` | varchar(200) |  |  |  |  | 发票下载接口地址 |
| `cSheng` | nvarchar(10) |  |  |  |  | 省份 |
| `cInsuranceLogoUrl` | varchar(500) |  |  |  |  | 机构LOGO地址 |
| `cPartnerName` | varchar(100) |  |  |  |  | 合作机构名称 |
| `cApiParametersPush` | varchar(3000) |  |  |  |  | 接口参数拼接 |
| `evisePolicyApiUrl` | varchar(100) |  |  |  |  | 机构批改接口地址 |
| `fIsGetXiaoShouXinXi` | tinyint |  |  | 否 | 1 | 是否传传销售信息，1是，0否 |
| `isChangebidStartTime` | tinyint |  |  | 否 | 1 | 是否要修改保险起止日期，1是 |
| `clauseCode` | varchar(30) |  |  |  |  | 机构条款代码 |
| `fIsGetFuJiaXian` | tinyint |  |  | 否 | 0 | 是否带有附加险，1是 |
| `fUseBidName` | tinyint |  |  | 否 | 0 | 是否用标段名称来代替项目名称，1是 |
| `cRemarks` | nvarchar(50) |  |  |  |  | 备注 |
| `downPolicyOFDApiUrl` | varchar(100) |  |  |  |  | 下载OFD接口地址 |
| `invoice_appApiUrl` | varchar(100) |  |  |  |  | 发票申请接口地址 |
| `greetingApiUrl` | varchar(100) |  |  |  |  | 承保接口地址 |
| `fIsImmediate` | tinyint |  |  | 否 | 0 | 是否即时起保，1是，2（宜宾）tender_start_time字段0时为起保，3（德阳）bzjenddate_encryption为起保，4第2天0时起保，22tender_start_time起保，大于等于值5，作为延迟几分钟，22（玉环）tender_start_time字段为起保 |
| `fisChangebidStartTimeType` | tinyint |  |  | 否 | 0 | 标的日期启用类型，0出单后第2天0点，1开标时间当天（格式"yyyy-MM-dd 00:00:00"），2开标时间当天（格式2005-11-05T14:30:00.000+0800） |
| `fEndorRequestType` | tinyint |  |  | 否 | 13 | 批改次数，13一次批改，25三次批改 |
| `claimsSettlementChannel` | varchar(20) |  |  |  |  | 是否开通理赔绿色通道的字段,0否 |
| `fStartAddCountTime` | int |  |  | 否 | 1 | 没有开标时间的话，第2天0点起保，即出单时间加上的天数 |
| `regionCode` | varchar(20) |  |  |  |  | 区域码，老核心下载OFD有用到 |
| `cBusinessId` | varchar(20) |  |  |  |  | 立项编码，值999时招标文件编号 |
| `cMobileMsg` | varchar(20) |  |  |  |  | 值1| 发出函短信通知 |
| `policySurrenderApiUrl` | varchar(100) |  |  |  |  | 退保接口地址 |
| `frequency` | tinyint |  |  |  |  | 1、批改后不需要拼接，2、批改在原ofd的文件上拼接一个新的ofd文件 |
| `identifyNumber` | varchar(20) |  |  |  |  | 加密保单上显示的投保人代码，为空则显示999999 |
| `fJoin` | tinyint |  |  | 否 | 0 | 1、广安拼接模式，项目名称=项目名称(标段名称)，项目编号=项目编号(标段编号)；2、宜宾模式，3、郴州OFD模式，4、广元模式，5、绵阳模式，6、内蒙模式 |
| `cSurrenderCode` | varchar(50) |  |  |  |  | 退保附加条款的编号，目前郴州 |
| `cPushCentralApi` | varchar(350) |  |  |  |  | 调用推送中心接口 |
| `cFuJiaXianCode` | varchar(30) |  |  |  |  | 附加险码 |
| `fEncryption` | tinyint |  |  | 否 | 0 | 保单里字段加密类型，0不加密，1通过SM4加密，2绵阳 |
| `fAttachmentType` | tinyint |  |  | 否 | 0 | 传附件模式，默认0无，1湖州下载OFD接口里传《投保单》签章文件，2（内蒙）、3（广元）、4（绵阳） |
| `file_uploadApiUrl` | varchar(100) |  |  |  |  | 影像上传接口地址 |
| `underlineQueryApiUrl` | varchar(100) |  |  |  |  | 线下转账查询接口 |
| `fFieldSaveType` | tinyint |  |  |  | 0 | 保存值类型，1和31（insuranceStartDate，insuranceEndDate），2（fMainCo=1） |
| `fChkJiBenHu` | tinyint |  |  | 否 | 1 | 请求保司接口，是否要验证基本户信息，默认1是，0否 |
| `policyQueryApiUrl` | varchar(100) |  |  |  |  | 保函查询接口 |

## T_Project_Apply

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `fProjectID` | int |  |  | 否 | 0 | 项目标段编号 |
| `cProjectGuid` | varchar(50) | 是 |  | 否 |  | 项目guid |
| `cUUID` | varchar(60) |  |  | 否 |  | 项目uuid |
| `tdate` | datetime |  |  | 否 | getdate() |  |

## T_PProduct_PayLog

*支付记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `transno` | varchar(50) | 是 |  | 否 |  | 银行流水号 |
| `transtime` | datetime |  |  | 否 |  | 支付时间 |
| `transamount` | decimal(18,2) |  |  | 否 |  | 支付金额 |
| `payeracctno` | varchar(50) |  |  | 否 |  | 付款卡号 |
| `payeracctname` | nvarchar(50) |  |  | 否 |  | 付款户名 |
| `abstractinfo` | nvarchar(50) |  |  |  |  | 备注 |
| `oppositebankno` | varchar(50) |  |  | 否 |  | 付款行号 |
| `oppositebankname` | nvarchar(50) |  |  | 否 |  | 付款行名 |
| `tdate` | datetime |  |  | 否 | getdate() | 日期 |
| `OrderNo` | varchar(50) |  |  |  |  | 订单号 |
| `fState` | tinyint |  |  | 否 | 0 | 0:未使用，1：已使用，2：退款中，3：已退款 |
| `cardType` | tinyint |  |  | 否 | 0 | 付款卡归属，0：中惠，1：湖南人保 |
| `skAccount` | varchar(50) |  |  | 否 | '' |  |
| `cAuditUserName` | nvarchar(50) |  |  |  |  |  |
| `cAuditMessage` | nvarchar(100) |  |  |  |  |  |
| `cAuditTime` | datetime |  |  |  |  |  |
| `fIsTestPay` | tinyint |  |  | 否 | 0 |  |

## T_Guarantee_InterfaceTransNos

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cNewGuid` | varchar(50) | 是 |  | 否 |  | 外键关联保单表Guarantee的cNewGuid |
| `InterfaceTrasNo1` | varchar(50) |  |  |  |  | 接口1交易流水号(各接口编号根据实际自行编排，岳阳：  baohanapply=1,
            baohanInvoice=2,//该接口不需要流水
            baohanRestore=3,
            baohanDisable=4,
            baohanClaim=5,
            baohanRevoke=6) |
| `InterfaceTrasNo2` | varchar(50) |  |  |  |  |  |
| `InterfaceTrasNo3` | varchar(50) |  |  |  |  |  |
| `InterfaceTrasNo4` | varchar(50) |  |  |  |  |  |
| `InterfaceTrasNo5` | varchar(50) |  |  |  |  |  |
| `InterfaceTrasNo6` | varchar(50) |  |  |  |  |  |
| `InterfaceTrasNo7` | varchar(50) |  |  |  |  |  |
| `InterfaceTrasNo8` | varchar(50) |  |  |  |  |  |
| `InterfaceTrasNo9` | varchar(50) |  |  |  |  |  |

## T_Account_Info

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cAccountName` | nvarchar(50) |  |  |  |  | 收款账户名称 |
| `cAccountCard` | nvarchar(50) |  |  |  |  | 收款账户卡号 |
| `cAccountBank` | nvarchar(50) |  |  |  |  | 收款账户银行 |
| `cUseInsurance` | nvarchar(MAX) |  |  |  |  | 使用机构 ,隔开 |
| `cConfigAbout` | nvarchar(500) |  |  |  |  | 配置依据 |
| `cSendMode` | nvarchar(50) |  |  |  |  | 短信通道 |
| `cSendSign` | nvarchar(50) |  |  |  |  | 短信签名 |
| `tCreateTime` | datetime |  |  |  |  | 添加时间 |
| `cEditUser` | nvarchar(50) |  |  |  |  | 最后编辑人 |
| `fSendTemplate` | int |  |  |  |  | 发送模板 |

## T_Guarantee_BidInfo

*订单标段表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fGuaranteeID` | int |  |  | 否 | 0 | 保单表id |
| `fProjectID` | int |  |  | 否 | 0 | 项目表id |
| `cBidId` | varchar(150) |  |  |  |  | 标段编号 |
| `cBidName` | nvarchar(600) |  |  |  |  | 标段名称 |
| `fMarginAmount` | decimal(18,2) |  |  |  |  | 标段保证金金额 |
| `CreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |

## T_OfflineOperationLog

*线下操作日志表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `MgrId` | int |  |  | 否 |  | 管理员ID |
| `SecondIden` | varchar(20) |  |  |  |  | 辅助标识 |
| `TargetTable` | varchar(50) |  |  | 否 |  | 操作表对象 如Project_Info |
| `TargetId` | int |  |  |  |  | 操作对象ID |
| `OptType` | tinyint |  |  | 否 |  | 操作类型  1.添加2.删除3.查询4.编辑 5.发布 6.延期 7.审核 |
| `IP` | varchar(50) |  |  |  |  | IP 地址 |
| `OptDateTime` | datetime |  |  |  |  | 操作时间 |

## T_Project_DelayLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  | 项目延期记录表 |
| `fProjectID` | int |  |  |  |  | 项目表id |
| `tOldBidTime` | datetime |  |  |  |  | 原开标时间 |
| `tNewBidTime` | datetime |  |  |  |  | 新开标时间 |
| `cRemark` | nvarchar(500) |  |  |  |  | 延期原因 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 操作时间 |
| `fUserID` | int |  |  | 否 | 0 | 操作用户id |
| `SecondIden` | varchar(20) |  |  |  |  | 辅助标识（操作手机号） |

## T_ZX_ProductInquiryClaim

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cInquiryGuid` | varchar(50) | 是 |  | 否 |  |  |
| `claim_reason` | nvarchar(200) |  |  |  |  |  |
| `cPolicyNo` | nvarchar(50) |  |  |  |  |  |
| `receive_bank_name` | nvarchar(100) |  |  |  |  |  |
| `receive_account_name` | nvarchar(100) |  |  |  |  |  |
| `receive_bank_no` | varchar(50) |  |  |  |  |  |
| `amount` | decimal(18,2) |  |  |  |  |  |
| `agent_name` | nvarchar(100) |  |  |  |  | 联系人 |
| `agent_phone` | varchar(20) |  |  |  |  |  |
| `claim_evidence_url` | nvarchar(1000) |  |  |  |  | 理赔材料 |
| `IsSent` | tinyint |  |  |  |  | 是否已发送（默认0未发送，1已发送) |
| `createTime` | datetime |  |  | 否 | getdate() |  |
| `fClaimState` | int |  |  |  |  | 理赔状态 0 待处理 1已通过 2已驳回 |
| `reject_reson` | nvarchar(200) |  |  |  |  | 拒绝原因 |
| `tPushTime` | datetime |  |  |  |  | 推送时间 |

## T_PProduct_PaymentVouchers

*上传凭证记录*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  | 0 |  |
| `fGuaranteeInfoID` | int |  |  |  | 0 | 保单表ID |
| `fProjectID` | int |  |  |  | 0 | 项目表ID |
| `cPaymentNo` | nvarchar(100) |  |  |  |  | 上传凭证序列号 |
| `cPaymentUrl` | nvarchar(100) |  |  |  |  | 凭证上传地址 |
| `CreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `fIsSend` | tinyint |  |  |  | 0 |  |
| `cAuditMessage` | nvarchar(50) |  |  |  |  |  |
| `cAuditUserName` | nvarchar(50) |  |  |  |  |  |
| `cAuditTime` | datetime |  |  |  |  |  |

## T_AliAuthorizeSecurity_Records

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cIP` | varchar(20) |  |  | 否 |  |  |
| `cType` | nvarchar(20) |  |  | 否 |  | 来源（WZ：温州；  HZ09：杭州9楼；   HZ20：杭州20楼） |
| `tCreateDate` | datetime |  |  |  | getdate() |  |
| `fIsDelete` | tinyint |  |  |  | 0 | 是否删除（0：否；1：是） |
| `tLastModiftDate` | datetime |  |  |  |  |  |

## T_PProduct_CheckLog

*多险种初审复核记录*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  |  |  | 关联外键 |
| `cBeforeLog` | varchar(300) |  |  |  |  | 修改前记录 |
| `cAfterLog` | varchar(300) |  |  |  |  | 修改后记录 |
| `fTag` | tinyint |  |  |  | 0 | 标签，1核保初审复核 |
| `tDate` | datetime |  |  |  | getdate() |  |

## T_GzZrx_UserMoenyRecord

*雇主责任险-用户资金记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cUserId` | varchar(50) |  |  |  |  | 余额账号用户ID，关联T_GzZrx_Users表ID |
| `fAmountType` | tinyint |  |  |  | 0 | 资金收支类型，1收入，2支出 |
| `fAmount` | decimal(10,2) |  |  |  | 0 | 金额 |
| `fRemainAmount` | decimal(10,2) |  |  |  | 0 | 剩余金额 |
| `cRemarks` | nvarchar(1000) |  |  |  |  | 备注信息 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `fAmountUseType` | tinyint |  |  |  | 0 | 资金用途：1余额调整，2保费支付 |
| `fLogID` | int |  |  |  | 0 | 日志表ID，关联T_GzZrx_OperationLog表ID |

## T_Project_FixLog

*项目特殊维护记录*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fProjectID` | int |  |  | 否 |  |  |
| `tfixDataDetail` | nvarchar(4000) |  |  | 否 |  |  |
| `tfixReason` | nvarchar(500) |  |  |  |  |  |
| `fUserID` | int |  |  | 否 | 0 |  |
| `SecondIden` | varchar(20) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_Epoint_PushGuaranteeImportLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `OperationTime` | datetime |  |  |  |  | 操作时间 |
| `Operator` | nvarchar(50) |  |  |  |  | 操作人 |
| `DataFileName` | nvarchar(200) |  |  |  |  | 数据Excel文件名 |
| `DataFilePath` | nvarchar(500) |  |  |  |  | 数据Excel保存地址 |
| `PlatformId` | int |  |  |  |  | T_Epoint_PlatformConfig表ID |

## T_PProduct_Policy

*多险种保单凭证记录列表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fGuaranteeInfoID` | int |  |  |  |  | 保单表ID |
| `cPolicyNo` | varchar(50) |  |  |  |  | 保单号 |
| `cPolicyUrl` | varchar(300) |  |  |  |  | 保单地址 |
| `cPolicyNoPz` | varchar(50) |  |  |  |  | 凭证号 |
| `cPolicyPzUrl` | varchar(300) |  |  |  |  | 凭证地址 |
| `cProposalno` | varchar(50) |  |  |  |  | 投保单号 |
| `cEsignUrl` | varchar(300) |  |  |  |  | 投保单文件 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |
| `tGuaranteedTime_begin` | datetime |  |  |  |  | 保险期限 |
| `tGuaranteedTime_end` | datetime |  |  |  |  | 保险期限 |
| `fMarginAmount` | decimal(18,2) |  |  |  | 0 | 保险金额 |
| `fPremium` | decimal(18,2) |  |  |  | 0 | 保费 |
| `fRate` | decimal(18,4) |  |  |  | 0 | 费率 |

## T_AliPay

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `Prc_Code` | nvarchar(30) |  |  |  |  |  |
| `out_trade_no` | varchar(50) |  |  |  |  | 订单号 |
| `subject` | nvarchar(50) |  |  |  |  | 订单名称 |
| `total_amout` | decimal(10,2) |  |  |  | 0 | 付款金额 |
| `des` | nvarchar(250) |  |  |  |  | 订单描述 |
| `returnUrl` | varchar(300) |  |  |  |  | 同步回调地址 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |
| `trade_no` | varchar(100) |  |  |  |  | 支付宝交易号 |
| `trade_status` | varchar(50) |  |  |  |  |  |
| `total_fee` | decimal(10,2) |  |  |  | 0 | 交易金额 |
| `seller_id` | varchar(100) |  |  |  |  | 收款支付宝账号 |
| `paybacktime` | datetime |  |  |  |  | 异步回调时间 |
| `fState` | tinyint |  |  |  | 0 | 状态：0待支付，2同步回调失败，4同步回调成功，6异步回调支付失败，8异步回调支付成功 |

## T_pay_log_cardType

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `skAccount` | varchar(50) | 是 |  | 否 |  | 虚拟卡号 |
| `mdcard` | varchar(50) |  |  | 否 |  | 实体卡号 |
| `TypeNo` | tinyint |  |  | 否 |  | 类型编号，0：中惠，1：湖南人保，2：中惠农行，3：中惠北京工行，4：龙岩人保，5：中惠农行常州，6：鹿城联银担保，7：福建天安，8：江西农民工人保，9：泰顺联银担保，10：滁州天安（老卡号），11：深圳人保（老卡号），12：滁州天安(新)，13：瑞安桑农担保，14：中惠银企互联，15：平阳农商行，16：博州联银担保，17：温州总商会，18：中元保险经纪，19：鲲鹏保险经纪，20：漳州天安，21：深圳人保(新)，22：中移经纪，23，联银担保投保人加密，24：阿坝人保，25：诚泰保险，26：无锡担保，27：无锡担保宜兴分公司，28：无锡担保江阴分公司，29：三明天安，30：南平易顺担保，31：传化保险经纪，32：​四川双讯担保，33：福建迅捷担保，34：阿坝中华联，35：德阳中华联，36：千寻担保；37：广安国寿财；38：广安太保，39：云天担保 |
| `TypeName` | nvarchar(50) |  |  | 否 |  | 类型名称 |
| `prefix` | varchar(10) |  |  | 否 |  | 前缀 |
| `sysType` | tinyint |  |  | 否 |  | 系统类型，0：核心投标系统，1：代收代付系统，2：温州瓯e保，3：平阳瓯e保，4：鹿城瓯e保，5：多险种系统，6：省平台，7：安徽平台，8：佛山平台，9：宁德平台，10：安庆安责险，11：深圳信用险，12：无锡担保 |

## T_Guarantee_InsurancePayLog

*保司机构回调支付信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  |  |  | 订单表的订单号，即对应T_Guarantee_Info表cNewGuid |
| `pay_acc_name` | nvarchar(50) |  |  |  |  | 付款人名称 |
| `pay_acc_no` | varchar(50) |  |  |  |  | 付款账号 |
| `pay_acc_bankname` | nvarchar(50) |  |  |  |  | 付款账号所属银行 |
| `pay_time` | datetime |  |  |  |  | 支付时间 |
| `premium` | decimal(10,2) |  |  |  |  | 保费金额 |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `signDate` | datetime |  |  |  |  | 保司返回的签章日期 |
| `cPolicyNo` | varchar(50) |  |  |  |  | 保单号 |

## T_PProduct_PRC

*履约平台类型*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(50) |  |  | 否 |  | 客户经理 |
| `fPRCEnInsuranceID` | int |  |  | 否 |  | T_PProduct_PRCEnInsurance 表id |
| `tCreateDate` | datetime |  |  |  | getdate() |  |

## T_Bank_Flow

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `transno` | varchar(50) |  |  |  |  | 银行流水号 |
| `payeracctname` | nvarchar(100) |  |  |  |  | 付款户名 |
| `payeracctno` | varchar(50) |  |  |  |  | 付款卡号 |
| `transtime` | datetime |  |  |  |  | 支付时间 |
| `transamount` | decimal(18,2) |  |  |  | 0 | 支付金额 |
| `remainamount` | decimal(18,2) |  |  |  | 0 | 余额 |
| `cBankCardNo` | varchar(50) |  |  |  |  | 中惠银行账号 |
| `transType` | varchar(10) |  |  |  |  | 借/贷 |
| `prc_Code` | varchar(50) |  |  |  |  | 中心编码 |
| `insuranceName` | nvarchar(50) |  |  |  |  | 保险公司名称 |
| `cPolicyNo` | nvarchar(50) |  |  |  |  | 保单号 |
| `tGuaranteedTime` | datetime |  |  |  |  | 出函时间 |
| `fState` | tinyint |  |  |  | 0 | 状态：0默认无，1未支付，2未出函，3待支付，4已支付，5注销退款，6未出函退款，7退保已退款，8未出函已退款，9保费结算，10无关联，11保费预付款，12保险公司退款退保 ，14已出函注销退款，已出函注销退款已退款，99待退款 |
| `CreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `bz_type` | tinyint |  |  |  | 0 | 备注类型，0默认无，1未出函退款，2已出函退保退款，3保费结算，4其他 |
| `bz_transno` | varchar(50) |  |  |  |  | 备注关联流水号 |
| `bz_settlementNo` | varchar(50) |  |  |  |  | 备注关联结算单号 |
| `bz_info` | nvarchar(200) |  |  |  |  | 其他说明 |
| `bz_time` | datetime |  |  |  |  | 备注时间 |
| `fzt` | tinyint |  |  | 否 | 0 |  |
| `cSettlementNo` | varchar(50) |  |  |  |  | 保费结算单号 |
| `cRefund` | nvarchar(50) |  |  |  |  |  |
| `fBidTime` | datetime |  |  |  |  |  |
| `jsamountSum` | decimal(18,2) |  |  |  | 0 | 差额结算时，结算保费金额 |
| `jsType` | tinyint |  |  |  | 0 | 保费结算类型，默认0非差额结算，1差额结算 |

## T_Pay_Log_ImportLog

*工行支付导入日志表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cFileUrlName` | nvarchar(50) |  |  |  |  | 导入数据表文件名 |
| `cFileUrl` | varchar(300) |  |  |  |  | 导入数据表文件下载地址 |
| `cErr_FileUrlName` | nvarchar(50) |  |  |  |  | 导入错误数据表文件名 |
| `cErr_FileUrl` | varchar(300) |  |  |  |  | 导入错误数据表文件下载地址 |
| `fState` | tinyint |  |  |  | 0 | 导入状态：默认0未导入，1导入成功 |
| `cAuditUserName` | nvarchar(50) |  |  |  |  |  |
| `tdate` | datetime |  |  |  | getdate() |  |

## T_Enterprise_Data

*企业库表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cEnterpriseName` | nvarchar(50) |  |  | 否 |  | 企业名称 |
| `cEnterpriseNameCode` | varchar(50) |  |  | 否 |  | 企业统一社会信用代码 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_Project_InfoExtension

*项目拓展信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ProjectId` | int | 是 |  | 否 |  | 关联项目ID |
| `ExtendedJson` | nvarchar(MAX) |  |  | 否 |  | 项目拓展信息Json |
| `CreateTime` | datetime |  |  |  |  |  |
| `tLatestUpTime` | datetime |  |  |  |  |  |

## T_Bank_FlowRelation

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fBankFlowID` | int |  |  |  | 0 | 对应T_Bank_Flow表ID |
| `fBankFlowID_Relation` | int |  |  |  | 0 | 对应T_Bank_Flow表ID |
| `transno_Relation` | varchar(50) |  |  |  |  | 流水号 |
| `fState` | int |  |  |  | 0 | 状态 |
| `bz_type` | int |  |  |  | 0 | 备注类型 |
| `CreateTime` | datetime |  |  |  |  |  |
| `fBankFlowBztype` | int |  |  | 否 | 0 |  |

## T_ZX_ProductInquiryQuit

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cInquiryGuid` | varchar(50) |  |  |  |  |  |
| `cPolicyNo` | nvarchar(50) |  |  |  |  |  |
| `bank_name` | nvarchar(50) |  |  |  |  | 银行名称 |
| `bank_accountName` | nvarchar(50) |  |  |  |  | 退款账户名称 |
| `bank_no` | nvarchar(100) |  |  |  |  | 收款账号 |
| `amount` | decimal(18,2) |  |  |  |  |  |
| `contact_name` | nvarchar(100) |  |  |  |  | 联系人 |
| `contact_phone` | varchar(20) |  |  |  |  |  |
| `evidence_url` | nvarchar(1000) |  |  |  |  | 材料 |
| `reason` | nvarchar(200) |  |  |  |  |  |
| `fQuitState` | int |  |  |  |  | 状态 0 待处理 1已通过 2已驳回 |
| `IsSent` | tinyint |  |  |  |  | 是否已发送（默认0未发送，1已发送) |
| `createTime` | datetime |  |  | 否 | getdate() |  |
| `tPushTime` | datetime |  |  |  |  |  |

## T_Pay_Log_LiShui

*支付记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `transno` | varchar(50) | 是 |  | 否 |  | 银行流水号 |
| `transtime` | datetime |  |  | 否 |  | 支付时间 |
| `transamount` | decimal(18,2) |  |  | 否 |  | 支付金额 |
| `payeracctno` | varchar(50) |  |  | 否 |  | 付款卡号 |
| `payeracctname` | nvarchar(50) |  |  | 否 |  | 付款户名 |
| `abstractinfo` | nvarchar(50) |  |  |  |  | 备注 |
| `oppositebankno` | varchar(50) |  |  | 否 |  | 付款行号 |
| `oppositebankname` | nvarchar(50) |  |  | 否 |  | 付款行名 |
| `tdate` | datetime |  |  | 否 | getdate() | 日期 |
| `OrderNo` | varchar(50) |  |  |  |  | 订单号 |
| `fState` | tinyint |  |  | 否 | 0 | 0:未使用，1：已使用，2：退款中，3：已退款，4：付款异常 |
| `fisPush` | tinyint |  |  | 否 | 0 | 0:未推送，1：已推送 |
| `fGuaranteeInfoID` | int |  |  | 否 | 0 |  |
| `ErrorInfo` | nvarchar(50) |  |  |  |  | 失败原因 |

## T_ProJect_Result

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `bidno` | varchar(50) |  |  | 否 |  | 标段编号 |
| `bidname` | nvarchar(150) |  |  | 否 |  | 标段名称 |
| `tenderee` | nvarchar(150) |  |  | 否 |  | 招标人 |
| `kaibiaotime` | datetime |  |  | 否 |  | 开标时间 |
| `bidstatus` | tinyint |  |  | 否 |  | 1正常，2异常 |
| `biddername` | nvarchar(150) |  |  | 否 |  | 投标企业名称 |
| `biddercreditcode` | varchar(50) |  |  | 否 |  | 投标企业统一社会信用代码 |
| `toubaono` | varchar(50) |  |  | 否 |  | 投保编码 |
| `iszhongbiao` | tinyint |  |  | 否 |  | 是否中标 （1是,0否） |
| `platformcode` | varchar(50) |  |  | 否 |  | 平台编号 |

## T_PProduct_PRCEnInsuranceEnclosure

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCEnInsuranceID` | int |  |  |  |  | T_PProduct_PRCEnInsurance表ID |
| `fEnclosureID` | int |  |  |  |  | T_PProduct_Enclosure表ID |
| `cEnclosureName` | varchar(200) |  |  |  |  | 附件名称 |
| `cEnclosureCode` | varchar(150) |  |  |  |  | 附件编码 |
| `fIsUpLoad` | tinyint |  |  |  |  | 是否上传 |
| `fIsRequired` | tinyint |  |  |  |  | 是否必填 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cLastEditUser` | nvarchar(50) |  |  |  |  | 最后修改人 |
| `tLastEditTime` | datetime |  |  |  |  | 最后修改时间 |
| `fFlieType` | tinyint |  |  |  |  | 文件类型 1图片 2其他 |
| `cFileTempUrl` | varchar(200) |  |  |  |  |  |
| `cDisplayName` | nvarchar(100) |  |  |  |  |  |
| `cDesc` | nvarchar(100) |  |  |  |  |  |
| `fSort` | int |  |  |  |  |  |

## T_Bank_Info

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cBankCardNo` | varchar(50) | 是 |  | 否 |  | 中惠银行账号 |
| `cBankName` | nvarchar(50) |  |  |  |  | 中惠银行账号对应的银行户名 |
| `cStoredProcedure` | varchar(50) |  |  |  |  |  |
| `fOrderNum` | int |  |  | 否 | 0 |  |
| `fAccountType` | tinyint |  |  | 否 | 0 |  |

## T_Pay_NoUsed

*金华支付记录未使用*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `fGuaranteeInfoID` | int | 是 |  | 否 |  |  |
| `tdate` | datetime |  |  | 否 | getdate() |  |

## sysdiagrams

*1*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `name` | sysname |  |  | 否 |  |  |
| `principal_id` | int |  |  | 否 |  |  |
| `diagram_id` | int | 是 | 是 | 否 |  |  |
| `version` | int |  |  |  |  |  |
| `definition` | varbinary |  |  |  |  |  |

## T_Project_UpdateField

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fUpdateLogID` | int |  |  | 否 | 0 | T_Project_UpdateLog表id |
| `cChangeType` | nvarchar(20) |  |  |  |  | 变更类型 |
| `cOldValue` | nvarchar(100) |  |  |  |  | 旧值 |
| `cNewValue` | nvarchar(100) |  |  |  |  | 新值 |

## T_Bank_OutsidePlatform

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `transno` | varchar(50) | 是 |  | 否 |  | 银行流水号 |
| `Prc_Code` | varchar(50) |  |  | 否 |  | 平台编号 |
| `cInsuranceCompany` | nvarchar(50) |  |  | 否 |  | 承保机构 |
| `cPolicyNo` | varchar(50) |  |  | 否 |  | 保单号 |
| `tPolicyTime` | datetime |  |  | 否 |  | 承保时间 |
| `payeracctno` | varchar(50) |  |  | 否 |  | 支付帐号 |
| `transtime` | datetime |  |  | 否 |  | 付款到账时间 |
| `transamount` | decimal(10,2) |  |  | 否 |  | 付款金额 |
| `tdate` | datetime |  |  | 否 | getdate() |  |
| `fbidtime` | datetime |  |  |  |  |  |
| `cNewGuid` | varchar(100) |  |  |  |  |  |
| `fState` | tinyint |  |  |  |  |  |
| `fXkOrderID` | int |  |  |  | 0 |  |
| `fRate` | decimal(18,4) |  |  |  |  | 费率 |
| `cSourceCode` | nvarchar(50) |  |  |  |  | 渠道码 |

## T_GzZrx_QuitInfo

*雇主-退保信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fMainId` | int |  |  |  |  | T_GzZrx_GuaranteeMain 表 ID |
| `cPolicyNo` | nvarchar(50) |  |  |  |  | 保单号 |
| `cEnterpriseNo` | nvarchar(50) |  |  |  |  | 退保企业信用代码 |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 退保企业名称 |
| `fAmount` | decimal(18,2) |  |  |  |  | 退款金额 |
| `fEffectDate` | datetime |  |  |  |  | 退保生效时间 |
| `cApplyUser` | nvarchar(50) |  |  |  |  | 申请人 |
| `cRealName` | nvarchar(50) |  |  |  |  | 联系人 |
| `cPhone` | nvarchar(50) |  |  |  |  | 联系人手机号 |
| `fAuthDate` | datetime |  |  |  |  | 审核时间 |
| `cAuthUser` | nvarchar(50) |  |  |  |  | 审核人 |
| `tCreateDate` | datetime |  |  |  | getdate() |  |
| `fState` | tinyint |  |  |  | 0 | 退保状态 （0：待审核；1：已审核（已退保）；2：已撤销） |
| `cReturnNo` | nvarchar(50) |  |  |  |  | 退保单号 |
| `cReturnUrl` | nvarchar(300) |  |  |  |  | 退保批单文件 |
| `cReturnLocalUrl` | nvarchar(300) |  |  |  |  | 退保批单文件（OSS） |
| `tCancelTime` | datetime |  |  |  |  | 撤销时间 |
| `cCancelUser` | nvarchar(50) |  |  |  |  | 撤销人 |
| `fInsuranceType` | tinyint |  |  | 否 | 0 | 险种类型 0 雇主责任险 1 货运险 |

## T_PayLog_AuditLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPaylogID` | int |  |  |  | 0 | 支付记录表ID |
| `fState` | tinyint |  |  |  |  | 2：退款中，3：已退款 |
| `cAuditMessage` | nvarchar(100) |  |  |  |  | 审核备注说明 |
| `cAuditUserName` | nvarchar(20) |  |  |  |  | 审核人 |
| `cFiles` | varchar(MAX) |  |  |  |  | 文件地址 |
| `CreateTime` | datetime |  |  |  |  |  |
| `cFrom` | nvarchar(50) |  |  |  |  |  |
| `cAuditType` | nvarchar(30) |  |  |  |  |  |
| `fRefundType` | tinyint |  |  | 否 | 0 |  |
| `cBankSummary` | nvarchar(8) |  |  |  |  |  |
| `fTransCount` | int |  |  | 否 | 1 |  |
| `fTransMoenySum` | decimal(18,2) |  |  | 否 | 0 |  |
| `cFileUrls` | varchar(MAX) |  |  |  |  |  |
| `cBaseAreaShi` | nvarchar(20) |  |  |  |  |  |
| `tFinishTime` | datetime |  |  |  |  |  |
| `fCollectionAccountID` | tinyint |  |  | 否 | 0 |  |
| `fIsTk` | tinyint |  |  | 否 | 0 |  |
| `fIsIcbc` | tinyint |  |  | 否 | 0 |  |
| `fAduitLogID` | int |  |  | 否 | 0 |  |
| `fType` | tinyint |  |  | 否 | 0 | 0未出单退款，1注销退款，2保费结算退保退款 |
| `fBusinessType` | tinyint |  |  | 否 | 0 |  |
| `fPaymentID` | int |  |  | 否 | 0 |  |

## T_PProduct_PRCEnInsuranceEngagedesc

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `fPRCEnInsuranceID` | int | 是 |  | 否 |  | T_PProduct_PRCEnInsurance表ID |
| `fInsuranceTypeID` | int | 是 |  | 否 |  | T_PProduct_Insurance表ID |
| `EngagedescContent` | nvarchar(2000) |  |  | 否 |  | 特约内容，带占位符 |
| `cTitle` | nvarchar(100) |  |  |  |  |  |
| `CreateTime` | datetime |  |  |  | getdate() |  |
| `cAuditUserName` | nvarchar(20) |  |  |  |  | 操作人 |
| `tUpdateTime` | datetime |  |  |  |  | 最新修改时间 |
| `EngagesIsNull` | tinyint |  |  | 否 | 0 | 特约节点是生效 默认0 传1则无效即特约节点会被移除 |

## T_PProductYz_PRC

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCID` | int |  |  |  |  | T_PProduct_PRCEnInsurance表ID |
| `fEnclosureID` | int |  |  |  |  | T_PProduct_Enclosure表ID |
| `cEnclosureName` | varchar(200) |  |  |  |  | 附件名称 |
| `cEnclosureCode` | varchar(50) |  |  |  |  | 附件编码 |
| `fIsUpLoad` | tinyint |  |  |  |  | 是否上传 |
| `fIsRequired` | tinyint |  |  |  |  | 是否必填 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cLastEditUser` | nvarchar(50) |  |  |  |  | 最后修改人 |
| `tLastEditTime` | datetime |  |  |  |  | 最后修改时间 |
| `fFlieType` | tinyint |  |  |  |  | 文件类型 1图片 2其他 |
| `cFileUrl` | varchar(300) |  |  |  |  | 附件模板url |
| `cFileTempUrl` | varchar(200) |  |  |  |  |  |
| `cDisplayName` | nvarchar(100) |  |  |  |  | 显示名称 |
| `cDesc` | nvarchar(100) |  |  |  |  | 备注 |
| `fSort` | int |  |  |  |  | 排序（正序） |

## T_Bank_PayLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cPayAccNo` | varchar(50) |  |  | 否 |  | 付款人账号 |
| `cPayAccNameCN` | nvarchar(50) |  |  | 否 |  | 付款人姓名 |
| `cRecAccNo` | varchar(50) |  |  | 否 |  | 收款人账号 |
| `cRecAccNameCN` | nvarchar(50) |  |  | 否 |  | 收款人姓名 |
| `fPayAmt` | int |  |  | 否 |  | 支付金额（单位分） |
| `cSeqno` | varchar(50) |  |  | 否 |  | 指令包序列号 |
| `ciSeqno` | varchar(50) |  |  | 否 |  | 流水号 |
| `fSysIOFlg` | tinyint |  |  | 否 |  | 系统内外标志（1：系统内；2：系统外） |
| `fProp` | tinyint |  |  |  |  | 对公对私标志（0：对公账户；1：个人账户） |
| `cRecCityName` | nvarchar(50) |  |  |  |  | 收款方所在城市名称 |
| `cRecBankName` | nvarchar(60) |  |  |  |  | 交易对方银行名称 |
| `tCreateDate` | datetime |  |  |  | getdate() |  |
| `fResult` | tinyint |  |  |  | 0 | 是否支付成功（0：待提交银行处理；1：成功；2：失败；3：银行处理中） |
| `cResultMsg` | nvarchar(200) |  |  |  |  | 支付结果信息 |
| `fIsPush` | tinyint |  |  |  | 0 | 是否推送（0：未推送；1：已推送） |
| `tPushTime` | datetime |  |  |  |  | 推送时间 |
| `tPushSuccessTime` | datetime |  |  |  |  | 推送成功时间 |
| `cPushErrorMsg` | nvarchar(200) |  |  |  |  | 推送失败原因 |
| `cCallBackUrl` | nvarchar(500) |  |  |  |  | 消息推送地址 |
| `SerialNo` | varchar(100) |  |  |  |  | 支付接口返回的序列号，用于查询 |
| `UseCN` | nvarchar(500) |  |  |  |  | 用途备注（跨行对私必填） |
| `tPaySuccessTime` | datetime |  |  |  |  | 支付成功时间 |

## T_ZX_ProductInquiry

*振鑫产品询价表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Id` | int |  | 是 | 否 |  |  |
| `cInquiryGuid` | varchar(50) |  |  |  |  |  |
| `userid` | nvarchar(50) |  |  |  |  |  |
| `cBank` | nvarchar(100) |  |  |  |  | 基本户开户行名称 |
| `cBankCardNo` | varchar(100) |  |  |  |  | 基本户卡号 |
| `cBankAccountName` | nvarchar(100) |  |  |  |  |  |
| `guarantee_type` | int |  |  |  |  | 投保类型， 必填 0:投标履约 1:施工履约保函 2:农民工工资保函 3:工程款支付保函 4:工程质量保证保函 5:安全生产责任险 默认 0 |
| `tBidWinTime` | datetime |  |  |  |  | 中标结果公告发布时间 |
| `cProjectNo` | nvarchar(200) |  |  |  |  | 项目编号 |
| `bzjenddate` | datetime |  |  |  |  | 保证金缴纳截止时间 |
| `tPublishTime` | datetime |  |  |  |  | 项目发布时间 |
| `plannedDuration` | nvarchar(50) |  |  |  |  | 计划工期,有单位，如23（ 日历天）. （日历天） 、 （ 日历周） 等， 有可能 "-" |
| `projectPrice` | nvarchar(50) |  |  |  |  | 项目预计造价 可能为"-" |
| `projectAddress` | nvarchar(800) |  |  |  |  | 项目建设地点 |
| `projectType` | varchar(10) |  |  |  |  | 招标项目类别,必填,枚举： 建筑设计-A01;市政设计-A02;园林绿化-A98;公路-A03;采购-A04;水运-A06;其他-A99 |
| `fFender_expire` | int |  |  |  |  | 投保有效期 天 |
| `cBiddingNoticeUrl` | varchar(MAX) |  |  |  |  | 招标公告地址 |
| `cBiddingDocUrl` | varchar(MAX) |  |  |  |  | 招标文件地址 |
| `cOwnerUnit` | nvarchar(50) |  |  |  |  |  |
| `cOwnerUnitCode` | nvarchar(50) |  |  |  |  |  |
| `cOwnerContactUserTel` | varchar(50) |  |  |  |  |  |
| `cOwnerContactUserName` | varchar(50) |  |  |  |  |  |
| `cOwnerBankCardNo` | varchar(50) |  |  |  |  |  |
| `cOwnerBank` | varchar(50) |  |  |  |  |  |
| `cOwnerAccount` | varchar(50) |  |  |  |  |  |
| `cOwnerCompanyTel` | varchar(50) |  |  |  |  | 招标人公司联系电话 |
| `cOwnerAddress` | nvarchar(100) |  |  |  |  |  |
| `cApprovalCode` | nvarchar(100) |  |  |  |  | 项目审批编号 |
| `cContactUserName` | nvarchar(30) |  |  |  |  | 联系人名称 |
| `cCompanyAddress` | varchar(100) |  |  |  |  | 企业地址 |
| `cEmail` | varchar(50) |  |  |  |  |  |
| `cCorporationName` | nvarchar(20) |  |  |  |  | 法人姓名 |
| `cCorporationIDCard` | nvarchar(20) |  |  |  |  |  |
| `cCorporationPhone` | nvarchar(50) |  |  |  |  |  |
| `cLicenseUrl` | varchar(1000) |  |  |  |  | 营业执照地址 |
| `cEsignUrl` | nvarchar(300) |  |  |  |  | 签章地址 |
| `cProjectAgency` | nvarchar(1000) |  |  |  |  | 招标代理机构名称 |
| `tCreateTime` | datetime |  |  |  | getdate() |  |
| `tPlannedStartDate` | datetime |  |  |  |  | 计划开工日期 |
| `tPlannedEndDate` | datetime |  |  |  |  | 计划完工日期 |
| `cProjectTypeName` | nvarchar(30) |  |  |  |  | 项目类型中文名称 |
| `fBuildingArea` | decimal(18,2) |  |  |  |  | 建筑面积 |

## T_Payment_Vouchers

*上传凭证记录*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  | 0 |  |
| `fGuaranteeInfoID` | int |  |  |  | 0 | 保单表ID |
| `fProjectID` | int |  |  |  | 0 | 项目表ID |
| `cPaymentNo` | nvarchar(100) |  |  |  |  | 上传凭证序列号 |
| `cPaymentUrl` | nvarchar(100) |  |  |  |  | 凭证上传地址 |
| `CreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `fIsSend` | tinyint |  |  | 否 | 0 |  |
| `cAuditMessage` | nvarchar(50) |  |  |  |  |  |
| `cAuditUserName` | nvarchar(50) |  |  |  |  |  |
| `cAuditTime` | datetime |  |  |  |  |  |

## T_GzZrx_ExportList

*导出记录列表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(50) |  |  | 否 |  | 文件名称 |
| `tCreateDate` | datetime |  |  |  | getdate() | 创建时间 |
| `tStartTime` | datetime |  |  |  |  | 导出完成时间 |
| `tFinishTime` | datetime |  |  |  |  | 导出完成时间 |
| `cUrl` | nvarchar(500) |  |  |  |  | 下载地址 |
| `cError` | nvarchar(MAX) |  |  |  |  | 报错信息 |
| `cUser` | nvarchar(50) |  |  |  |  | 操作人 |
| `cFields` | nvarchar(500) |  |  |  |  | 查询字段 |
| `cWhere` | nvarchar(500) |  |  |  |  | 查询条件（sql查询用） |
| `cParam` | nvarchar(500) |  |  |  |  | 查询参数 |
| `fState` | tinyint |  |  |  | 0 | 状态（0：未处理；1：处理中；2：处理成功；3：处理失败；） |
| `whereStrName` | nvarchar(500) |  |  |  |  | 搜索条件（显示用） |
| `cUserID` | nvarchar(50) |  |  |  |  |  |
| `fEnterpriseID` | int |  |  |  |  |  |
| `fCount` | int |  |  |  |  | 记录数 |
| `fType` | tinyint |  |  |  |  | 类型（1：雇员信息导出；2：批单-批改雇员-页面导出；3：批单-批改雇员-支付-页面导出；4：办理保单页面导出；5：我的保单导出；6：我的批单导出； 7：退保审核导出） |

## T_Coupon_WriteOffLog

*优惠券核销记录*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fZXUserID` | int |  |  |  |  | 关联T_ZX_User表ID |
| `fEnterpriseInfoID` | int |  |  |  |  | 企业表ID |
| `fCouponID` | int |  |  |  | 0 | 关联T_Coupon_Info表ID |
| `tWriteOffTime` | datetime |  |  |  |  | 核销时间 |
| `cRemark` | nvarchar(350) |  |  |  |  | 备注 |
| `cUser` | nvarchar(20) |  |  |  |  | 发放人员 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |

## T_Coupon_Type

*优惠券类型表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cNum` | varchar(30) |  |  |  |  | 优惠券ID，编码 |
| `cName` | nvarchar(30) |  |  |  |  | 优惠券名称 |
| `cTitle` | nvarchar(50) |  |  |  |  | 标题备注 |
| `cDes` | nvarchar(300) |  |  |  |  | 描述 |
| `fFeeType` | tinyint |  |  |  | 0 | 费用类型，默认0费率折扣，1现金减免 |
| `fRate` | decimal(10,2) |  |  |  | 0 | fFeeType=0 费率折扣 |
| `fMoney` | decimal(10,2) |  |  |  | 0 | fFeeType=1 费用金额，fFeeType=0 对应折扣金额 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |
| `platformcode` | varchar(50) |  |  | 否 |  | 平台编码 |
| `fCount` | int |  |  |  | 0 | 可获得次数 |
| `cEvent` | varchar(30) |  |  |  |  | 事件 |
| `tStartTime` | datetime |  |  |  |  | 有效期开始时间 |
| `tEndTime` | datetime |  |  |  |  | 有效期结束时间 |
| `fDayInt` | int |  |  | 否 | 0 | 有效期需结合cUnit，值当为0时，有效期看tStartTime和tEndTime，不为0时，（非手动发放情况下，有效结束期为发放当日加当前值）（手动发放情况下，有效结束期为生效日期加当前值） |
| `cUnit` | varchar(10) |  |  |  |  | 单位：天、月、年 |
| `fReType` | tinyint |  |  | 否 | 0 | 发放方式，默认0系统自动发放(注册绑定)，1要求奖励发放(活动邀请)，2客服手动发放 |
| `fThresholdAmount` | decimal(10,2) |  |  | 否 | 0 | 使用门槛金额 |
| `fZt` | tinyint |  |  | 否 | 0 | 状态，0禁用，1启用 |
| `cUser` | nvarchar(20) |  |  |  |  | 发放人员 |
| `fGrantCount` | int |  |  |  | 0 | 客服手动发放数量 |
| `fWriteOff` | tinyint |  |  | 否 | 0 | 核销方式，默认0系统自动核销，1客服手动核销 |

## T_Push_Log

*项目推送获取日志表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fTag` | tinyint |  |  |  |  | 标签:1项目 |
| `cMsg` | nvarchar(200) |  |  |  |  |  |
| `CreateTime` | datetime |  |  |  | getdate() |  |
| `fGuaranteedID` | int |  |  |  | 0 |  |
| `cPostJson` | varchar(MAX) |  |  |  |  |  |
| `cResultJsonData` | varchar(MAX) |  |  |  |  |  |

## T_PProduct_ApplyRemind

*多险种-业务申请提醒信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `cBusiness_Code` | varchar(50) |  |  | 否 |  | 中心业务号，业务约定编号，唯一标识 |
| `tCreateTime` | datetime |  |  |  | getdate() | getdate() |
| `cInsuranceTypeNo` | varchar(30) |  |  |  |  |  |
| `cInsuranceCompany` | varchar(30) |  |  |  |  |  |
| `cPRCCode` | varchar(30) |  |  |  |  |  |
| `uuid` | varchar(50) | 是 |  | 否 |  | 表内唯一标识 |
| `fIsPush` | tinyint |  |  |  | 0 | 保函状态。默认0未获取申请信息，6已获取申请信息，1-已通知已受理，2-已通知不受理，3-已通知出函，7中心通知已放弃 |
| `tPushTime` | datetime |  |  |  |  | 获取时间 |
| `cErrMsg` | nvarchar(500) |  |  |  |  | 错误信息提示 |
| `fGUA_TYPE` | tinyint |  |  |  |  | 保函类型：0-投标保函1-预付款保函2-履约保函3-农民工工资保函 4-业主保函 5-质量保函 |
| `tag` | tinyint |  |  |  | 0 |  |

## T_PProduct_PRCEnInsuranceRegulator

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fRegulatorID` | int |  |  |  |  |  |
| `cName` | nvarchar(50) |  |  |  |  | 监管单位名称 |
| `cCode` | nvarchar(50) |  |  |  |  | 监管单位编码 |
| `cProvinceName` | nvarchar(50) |  |  |  |  | 监管单位省名称 |
| `cProvinceCode` | nvarchar(50) |  |  |  |  | 监管单位省编码 |
| `cCityName` | nvarchar(50) |  |  |  |  | 监管单位城市名称 |
| `cCityCode` | nvarchar(50) |  |  |  |  | 监管单位城市编码 |
| `cAreaName` | nvarchar(50) |  |  |  |  | 监管单位区名称 |
| `cAreaCode` | nvarchar(50) |  |  |  |  | 监管单位区编码 |
| `fPRCEnInsuranceID` | int |  |  |  |  | T_PProduct_PRCEnInsurance表ID |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cBeneficiary` | nvarchar(50) |  |  |  |  | 受益人 |

## T_Base_Area

*行政区划编码表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cCode` | varchar(10) |  |  | 否 |  |  |
| `cParentCode` | varchar(10) |  |  |  |  |  |
| `cName` | nvarchar(50) |  |  | 否 |  |  |
| `fLevel` | int |  |  |  |  |  |

## T_PaymentSystem_Cancel

*退保记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `applyno` | varchar(50) | 是 |  | 否 |  |  |
| `tdate` | datetime |  |  | 否 | getdate() |  |
| `fState` | tinyint |  |  | 否 | 0 | 0：未发送（未处理），1：已发送（已处理），2：处理完成（其他退款） 3：处理完成(保费结算退保退款) |
| `tsubdate` | datetime |  |  |  |  |  |
| `cAuditUserName` | nvarchar(50) |  |  |  |  | 操作人 |
| `fType` | tinyint |  |  | 否 | 0 | 1：手动添加；0：接口推送 |

## T_QuitGuarantee_Attachment

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(50) |  |  |  |  |  |
| `cCode` | varchar(20) |  |  | 否 |  |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |
| `fFileType` | tinyint |  |  | 否 | 1 |  |
| `fState` | tinyint |  |  | 否 | 1 |  |

## T_GzZrx_GLG

*公路港信息*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(50) |  |  | 否 |  |  |

## T_PProduct_PRCEnInsuranceTmpContent

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  |  |  |  |  |
| `fPRCEnInsuranceID` | int | 是 |  | 否 |  | T_PProduct_PRCEnInsurance表ID |
| `fInsuranceTypeID` | int | 是 |  | 否 |  | T_PProduct_Insurance表ID |
| `cContent` | nvarchar(3000) |  |  |  |  | 动态保函模板内容 |
| `cTitle` | nvarchar(100) |  |  |  |  | 标题 |
| `CreateTime` | datetime |  |  |  |  |  |
| `cAuditUserName` | nvarchar(20) |  |  |  |  | 操作人 |
| `tUpdateTime` | datetime |  |  |  |  | 最新修改时间 |

## T_Insurance_File

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fBaseID` | int |  |  |  |  |  |
| `cName` | nvarchar(50) |  |  |  |  |  |
| `cFileNumber` | varchar(50) |  |  |  |  |  |
| `cFileUrl` | varchar(200) |  |  |  |  |  |
| `fFileSaveType` | tinyint |  |  |  |  |  |
| `CreateTime` | datetime |  |  |  |  |  |
| `fOrder` | int |  |  |  |  |  |
| `cPosX` | varchar(30) |  |  |  |  |  |
| `cPosY` | varchar(30) |  |  |  |  |  |
| `cRemarks` | nvarchar(MAX) |  |  |  |  |  |
| `cProductTypeNo` | varchar(30) |  |  |  |  |  |
| `cProductNo` | varchar(30) |  |  |  |  |  |
| `fPosPage` | tinyint |  |  |  |  |  |
| `cContent` | nvarchar(2000) |  |  |  |  |  |
| `cFilePreviewUrl` | varchar(500) |  |  |  |  | 预览地址（振鑫手机端展示用png地址） |
| `fDaysType` | tinyint |  |  | 否 | 1 | 担保天数类型（1：固定天数；2：用户输入） |
| `fDays` | int |  |  | 否 | 0 | 担保天数 |
| `fExtendDays` | int |  |  | 否 | 0 | 扩展天数（担保小程序用到） |
| `cShowItems` | varchar(20) |  |  | 否 | '0,0,0,0' | 显示信息0：不显示；1：显示。（4个段位分别表示：项目名称，项目编号，标段名称，标段编号） |

## T_Base_File

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cNumber` | varchar(50) | 是 |  | 否 |  | 序列号编码 |
| `cName` | nvarchar(50) |  |  |  |  | 名称 |
| `fType` | tinyint |  |  |  | 0 | 类型，0承保业务附件类型 |
| `CreateTime` | datetime |  |  |  | getdate() |  |

## T_PaymentSystem_CancelLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `applyno` | varchar(50) |  |  | 否 |  |  |
| `cAuditUserName` | nvarchar(50) |  |  |  |  |  |
| `cOperationType` | nvarchar(50) |  |  |  |  |  |
| `cRemark` | nvarchar(200) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |
| `cUrl` | nvarchar(350) |  |  |  |  |  |

## T_PProduct_PRCIns

*渠道险种关联表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCID` | int |  |  |  |  | T_PProduct_PRC表ID |
| `fInsID` | int |  |  |  |  | T_PProduct_Insurance表ID |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cLastEditUser` | nvarchar(50) |  |  |  |  | 最后修改人 |
| `tLastEditTime` | datetime |  |  |  |  | 最后修改时间 |
| `fInsName` | nvarchar(50) |  |  |  |  | 险种名称 |

## T_PProduct_ExportStatisticalRecord

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cUserId` | uniqueidentifier |  |  |  |  |  |
| `tExportTime` | datetime |  |  |  |  |  |
| `cDataType` | nvarchar(200) |  |  |  |  | 导出数据类型 |
| `fExportCount` | int |  |  |  |  | 导出数据条数 |
| `cInsuranceType` | nvarchar(500) |  |  |  |  | 险种类型 |
| `cOrderTime` | nvarchar(50) |  |  |  |  | 订单时间 |
| `cLocation` | nvarchar(100) |  |  |  |  | 承保机构所在地 |
| `cInsuranceCompany` | nvarchar(1000) |  |  |  |  | 保司 |
| `cStatus` | nvarchar(100) |  |  |  |  | 申请状态 |
| `cGuaranteeTime` | nvarchar(50) |  |  |  |  | 出单时间 |
| `cExportFile` | nvarchar(300) |  |  |  |  | 导出文件 |
| `cUserName` | nvarchar(50) |  |  |  |  |  |

## T_Guarantee_extend

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cNewGuid` | varchar(50) | 是 |  | 否 |  |  |
| `insuranceStartDate` | datetime |  |  |  |  | 保险起期 |
| `insuranceEndDate` | datetime |  |  |  |  | 保险期止 |
| `insurancePeriod` | int |  |  |  |  | 保险期限(天) |
| `tdate` | datetime |  |  | 否 | getdate() |  |
| `cPolicyOfdUrl` | varchar(200) |  |  |  |  |  |
| `cPGPolicyOfdUrl` | varchar(200) |  |  |  |  |  |
| `tender_start_time` | datetime |  |  |  |  |  |
| `cContactIDType` | nvarchar(30) |  |  |  |  |  |
| `basic_need` | tinyint |  |  |  |  |  |
| `coinsuranceIdentification` | varchar(20) |  |  |  |  |  |
| `tender_bond_end_time` | datetime |  |  |  |  |  |
| `cCallbackUrl` | nvarchar(250) |  |  |  |  |  |
| `agent_name` | nvarchar(30) |  |  |  |  |  |
| `agent_phone` | nvarchar(30) |  |  |  |  |  |
| `cContactUserName` | nvarchar(30) |  |  |  |  | 招标人联系人 |
| `cContactUserTel` | nvarchar(30) |  |  |  |  | 招标人联系人联系方式 |
| `cOwnerSheng` | varchar(10) |  |  |  |  |  |
| `cOwnerShi` | varchar(10) |  |  |  |  |  |
| `cOwnerQu` | varchar(10) |  |  |  |  |  |
| `cOwnerNature` | varchar(10) |  |  |  |  |  |
| `fPolicyExtendDay` | int |  |  | 否 | 0 |  |
| `tPolicyLatestDate` | datetime |  |  |  |  |  |
| `fPGState` | tinyint |  |  | 否 | 0 |  |
| `fGLDPayPush` | tinyint |  |  | 否 | 0 |  |
| `fIsCancelPush` | tinyint |  |  |  |  |  |
| `fIsPayNotice` | tinyint |  |  |  |  |  |
| `fIsPaidNotice` | tinyint |  |  |  | 0 | 支付结果通知（个别地区需要，默认0 ，0未推送 1已推送） |
| `fIsInvalidNotice` | tinyint |  |  |  | 0 | 失效订单推送状态 0未推送 1 已推送 |
| `cEndorseText` | nvarchar(MAX) |  |  |  |  |  |
| `fIsPtextFlag` | tinyint |  |  | 否 | 0 |  |
| `cPaymentTransactionNo` | nvarchar(50) |  |  |  |  |  |
| `cToNshEsignUrl` | nvarchar(200) |  |  |  |  |  |
| `cNshEsignUrl` | nvarchar(200) |  |  |  |  |  |
| `qualifications` | nvarchar(150) |  |  |  |  |  |
| `cAccessKey` | nvarchar(50) |  |  |  |  |  |
| `tkIsPush` | tinyint |  |  | 否 | 0 |  |
| `jgQuitIsPush` | tinyint |  |  | 否 | 0 | 机构退保状态 0默认(待调用) 1 待调用 2 退保成功 3 待回调 |
| `yyzzfileguid` | varchar(64) |  |  |  |  |  |
| `biddername_encryption` | varchar(200) |  |  |  |  | 投保人(密文) |
| `biddercode_encryption` | varchar(200) |  |  |  |  | 投保人信用代码(密文) |
| `fIsFirmPush` | tinyint |  |  | 否 | 0 |  |
| `FirmPushSucTime` | datetime |  |  |  |  |  |
| `TerminalType` | varchar(5) |  |  |  | 'PC' |  |
| `biaoduanstatus` | tinyint |  |  | 否 | 0 | 标段状态 0 正常 1 流标 2 终止 3 暂停 4 作废 |
| `departmentcodechn` | varchar(30) |  |  |  |  |  |
| `GuaranteeAgreementUrl` | varchar(200) |  |  |  |  |  |
| `AttachmentIsDownload` | tinyint |  |  |  |  |  |
| `Attachment2IsDownload` | tinyint |  |  |  |  |  |
| `Attachment3IsDownload` | tinyint |  |  |  |  |  |
| `Attachment4IsDownload` | tinyint |  |  |  |  |  |
| `AttachmentId` | varchar(100) |  |  |  |  |  |
| `NoticeNo` | varchar(100) |  |  |  |  |  |
| `fDiscountId` | int |  |  | 否 | 0 |  |
| `discountIsReturn` | tinyint |  |  | 否 | 0 |  |
| `cOrderNo` | varchar(100) |  |  |  |  |  |
| `fDtUserID` | int |  |  | 否 | 0 |  |
| `tStartEffectiveTime` | datetime |  |  |  |  | 保险起期（对应T_Guarantee_Info表的止期tEffectiveTime） |
| `payerName` | nvarchar(50) |  |  |  |  | 付款人账户名称(平安支付回调) |
| `payerBankAccount` | nvarchar(50) |  |  |  |  | 付款人账号(平安支付回调） |
| `payMode` | nvarchar(50) |  |  |  |  | 付款类型（平安支付回调） |
| `skAccountName` | nvarchar(50) |  |  |  |  | 收款人账号，陕西西安省平台政采使用 |
| `cJbrIDCard` | varchar(50) |  |  |  |  |  |
| `cSheBaoUrl` | varchar(200) |  |  |  |  | 经办人社保证明url |
| `cJbrSFZUrl` | varchar(200) |  |  |  |  | 经办人身份证 |
| `cFaRenSQSUrl` | varchar(200) |  |  |  |  | 法人授权书 |
| `cFinancialUrl` | varchar(200) |  |  |  |  | 财务报表url |
| `cPMIntroUrl` | varchar(200) |  |  |  |  | 项目经理简介url |
| `cCommitLetterUrl` | varchar(200) |  |  |  |  | 承保书url |
| `fbhIsPush` | tinyint |  |  | 否 | 0 | 经纪机构数据交互推送状态 0 未推送 1 密文已推送 2 明文已推送 |
| `ftbIsPush` | tinyint |  |  | 否 | 0 | 经纪机构数据交互推送状态 0 退保未推送 1 退保已推送 |
| `cPGEsignUrl` | varchar(200) |  |  |  |  |  |
| `cPGErrorInfo` | nvarchar(200) |  |  |  |  |  |
| `fPolicyIsInvalid` | tinyint |  |  |  | 0 | 保单是否已失效 |
| `fBatchId` | int |  |  |  |  | 订单批次表id  （T_ZX_GuaranteeBatch，担保小程序用） |
| `fCouponMoney` | decimal(10,2) |  |  | 否 | 0 | 优惠券金额 |
| `fpayUrlCloseState` | tinyint |  |  | 否 | 0 | 前提条件:T_Guarantee_Info.State  = 14，15 ; 初始默认值= 0 ;如果已经将支付链接推送给保司,作废成功  =1 ;作废失败 = 2 |
| `tpayUrlEndTime` | datetime |  |  |  |  | 保司返回的支付链接有效期,在该时间之前有效,在该时间之后将无法支付,链接失效 |
| `cEnterpriseName_encryption` | varchar(500) |  |  |  |  |  |
| `cEnterpriseNameCode_encryption` | varchar(500) |  |  |  |  |  |
| `tUnderwritingTime` | datetime |  |  |  |  | 人工审核(核保)时间 |
| `tPubDate_encryption` | varchar(200) |  |  |  |  | 招标公告发布时间(密文) |
| `bidderaddress_encryption` | varchar(300) |  |  |  |  | 投保人地址(加密) |
| `cMD5HashCode` | varchar(50) |  |  |  |  |  |
| `cMD5HashCodePG` | varchar(50) |  |  |  |  |  |
| `fIsEsignUrlPush` | tinyint |  |  |  | 0 | 签章文件推送状态（0 默认未推送,1已推送）个别地方用到， |
| `cCreditReportUrl` | varchar(200) |  |  |  |  |  |
| `fPolicyTmpID` | int |  |  | 否 | 0 |  |
| `cPolicyTmp` | varchar(100) |  |  |  |  |  |
| `bzjamount_encryption` | varchar(50) |  |  |  |  |  |
| `skBank` | varchar(100) |  |  |  |  |  |
| `cProjectCode` | varchar(50) |  |  |  |  |  |
| `cApprovalCode` | varchar(50) |  |  |  |  |  |
| `cOwnerBankCardNo` | varchar(50) |  |  |  |  |  |
| `cOwnerBank` | nvarchar(50) |  |  |  |  |  |
| `fbhTechIsPush` | tinyint |  |  | 否 | 0 |  |
| `kaibiaotime_encryption` | nvarchar(200) |  |  |  |  |  |
| `fUsezbType` | tinyint |  |  |  |  | 保函文件类型 可为NULL 1 独立保函 2 非独立保函 |
| `skCardNumber` | varchar(50) |  |  |  |  | 对接保司收银台获取收款账户信息 |
| `cElectronicReceiptUrl` | nvarchar(230) |  |  |  |  | 电子收据到账凭证url-人保宜宾地区用到 |
| `cPushClosingStatus` | nvarchar(20) |  |  |  |  | 关闭订单的接口-是否已经推送给保司 |
| `cOpenId` | varchar(64) |  |  |  |  |  |
| `makeFlag` | nvarchar(50) |  |  |  |  |  |
| `remark` | nvarchar(100) |  |  |  |  |  |

## T_QuitGuarantee_AuditLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  |  |  | 关联订单表T_Guarantee_Info的cNewGuid |
| `cFileUrl` | varchar(200) |  |  |  |  | 文件地址 |
| `tCreateTime` | datetime |  |  |  | getdate() |  |

## T_Guarantee_Info

*投保单信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  | 否 |  |  |
| `cEnterpriseName` | nvarchar(200) |  |  |  |  | 企业名称 |
| `cEnterpriseNameCode` | nvarchar(100) |  |  |  |  | 统一社会信用代码 |
| `cCorporationName` | nvarchar(20) |  |  |  |  | 法人姓名 |
| `cBank` | nvarchar(50) |  |  |  |  | 基本户开户行 |
| `cBankCardNo` | varchar(50) |  |  |  |  | 基本户账号 |
| `fUserID` | int |  |  |  | 0 |  |
| `cRealName` | nvarchar(50) |  |  |  |  | 联系人姓名 |
| `cPhone` | nvarchar(100) |  |  |  |  | 联系人手机号码 |
| `cEmail` | varchar(50) |  |  |  |  | 联系人邮箱 |
| `cAddress` | nvarchar(100) |  |  |  |  | 联系人地址 |
| `fProjectID` | int |  |  |  |  | 项目信息表自增ID |
| `cToEsignUrl` | nvarchar(200) |  |  |  |  | 待签章文件地址 |
| `cEsignUrl` | nvarchar(200) |  |  |  |  | 投保单签章文件地址 |
| `tEsignTime` | datetime |  |  |  |  | 签章时间 |
| `fRate` | decimal(10,3) |  |  |  | 0 | 费率（%） |
| `fPremium` | decimal(18,2) |  |  |  | 0 | 保费(元) |
| `cPolicyNo` | nvarchar(50) |  |  |  |  | 人保保单号 |
| `cPolicyUrl` | varchar(500) |  |  |  |  | 人保保单下载地址 |
| `cPolicyLocalUrl` | varchar(500) |  |  |  |  | 人保保单本地地址 |
| `tReceivePolicyTime` | datetime |  |  |  |  | 人保保单接收时间 |
| `tPolicyTime` | datetime |  |  |  |  | 人保保单生成时间 |
| `fState` | tinyint |  |  |  | 0 | 状态（0默认未签章，2已签章，3付款未到账，4已付款，5付款异常，6已出函，10已出具发票 |
| `tGuaranteedTime` | datetime |  |  |  |  | 出函时间 |
| `cPaymentSerialNumber` | nvarchar(50) |  |  |  |  | 打款序列号 |
| `cPaymentVoucher` | nvarchar(100) |  |  |  |  | 付款凭证上传地址 |
| `tPaymentVoucherTime` | datetime |  |  |  |  | 付款凭证上传时间 |
| `CreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `UUID` | nvarchar(150) |  |  |  |  | 人保影像传递用 投保时生产uuid,影像接口需要再次用到 |
| `cPolicyZipUrl` | nvarchar(500) |  |  |  |  | 提供给人保下载的zip文件路径 |
| `cPolicyZipName` | nvarchar(100) |  |  |  |  | 提供给人保下载的zip文件名 |
| `cInsuranceCompany` | nvarchar(50) |  |  |  |  | 保险公司名称 |
| `tEffectiveTime` | datetime |  |  |  |  | 有效保函有效时间 |
| `fIsPush` | tinyint |  |  |  | 0 | 是否已经推送，默认0未推送，1推送成功,2:已推送加密保函，3保函已解密 |
| `tPushTime` | datetime |  |  |  |  | 推送时间 |
| `tPushSuccessTime` | datetime |  |  |  |  | 成功推送记录时间 |
| `cPayBank` | nvarchar(50) |  |  |  |  | 保费支付银行 |
| `cPayBankCardNo` | varchar(50) |  |  |  |  | 保费支付银行账号 |
| `tPayTime` | datetime |  |  |  |  | 保费支付时间 |
| `fAuditType` | tinyint |  |  |  |  | 0：自动审核，1：人工审核 |
| `tAuditTime` | datetime |  |  |  |  | 审核时间 |
| `cMac` | varchar(50) |  |  |  |  | 投标电脑MAC地址 |
| `cHardDisk` | varchar(50) |  |  |  |  | 投标电脑硬盘序列号 |
| `cCPU` | varchar(50) |  |  |  |  | 投标电脑CPU序列号 |
| `cIP` | varchar(50) |  |  |  |  | 投标电脑公网IP |
| `fPayId` | int |  |  |  |  |  |
| `cAuditMessage` | nvarchar(50) |  |  |  |  | 人工审核备注 |
| `cNewGuid` | varchar(50) |  |  | 否 |  | 唯一性标识 |
| `PolicyUpdateTime` | datetime |  |  |  |  | 保函文件下载时间 |
| `ErrorInfor` | nvarchar(200) |  |  |  |  | 异常信息 |
| `fzipIsPush` | tinyint |  |  | 否 |  | 推送ZIP文件，0：未打包，1：已打包，2：已推送 |
| `platformcode` | varchar(50) |  |  |  |  | 平台编码 |
| `cBidId_encryption` | varchar(500) |  |  |  |  | 标段编号密文 |
| `cBidName_encryption` | varchar(1000) |  |  |  |  | 标段名称密文 |
| `cOwnerUnit_encryption` | varchar(500) |  |  |  |  | 招标人密文 |
| `cOwnerUnitCode_encryption` | varchar(500) |  |  |  |  | 招标人统一社会编码密文 |
| `DecryptionKey` | varchar(50) |  |  |  |  | 解密密钥 |
| `fMarginAmount` | decimal(18,2) |  |  | 否 | 0 | 保证金金额 |
| `EndorseNo` | varchar(50) |  |  |  |  | 批单号 |
| `cPGPolicyUrl` | varchar(500) |  |  |  |  | 批单后的下载地址 |
| `cPGPolicyLocalUrl` | varchar(500) |  |  |  |  | 批单后的本地下载地址 |
| `cPGUUID` | varchar(60) |  |  |  |  | 批单UUID |
| `tPGTime` | datetime |  |  |  |  | 批改时间 |
| `cInsuranceCode` | varchar(64) |  |  |  |  |  |
| `cProposalno` | nvarchar(100) |  |  |  |  |  |
| `cPayurl` | varchar(800) |  |  |  |  |  |
| `cCompanyTel` | varchar(50) |  |  |  |  |  |
| `cCompanyAddress` | nvarchar(100) |  |  |  |  |  |
| `cOrderId` | varchar(50) |  |  |  |  |  |
| `tOrderTime` | datetime |  |  |  |  |  |
| `cPolicyPzUrl` | varchar(500) |  |  |  |  | 保险凭证下载地址 |
| `fGProjectId` | int |  |  | 否 |  |  |
| `fInvoiceType` | tinyint |  |  |  |  |  |
| `cPGPolicyPzUrl` | varchar(500) |  |  |  |  |  |
| `pushEvidence` | tinyint |  |  | 否 |  | 是否推送e签宝存证 0 否 1是 |
| `claimsState` | tinyint |  |  | 否 |  |  |
| `quitIsPush` | tinyint |  |  | 否 |  |  |
| `AreaCode` | varchar(50) |  |  |  |  |  |
| `tQuitApplyTime` | datetime |  |  |  |  |  |
| `fQuitState` | tinyint |  |  | 否 | 0 |  |
| `fCouponID` | int |  |  | 否 | 0 |  |
| `cCouponDes` | nvarchar(50) |  |  |  |  |  |
| `cAuditUserName` | nvarchar(50) |  |  |  |  |  |
| `fPayType` | int |  |  | 否 | 0 |  |
| `skAccount` | varchar(50) |  |  |  |  |  |
| `bzjenddate_encryption` | varchar(200) |  |  |  |  |  |
| `insuredcontactname_encryption` | varchar(200) |  |  |  |  |  |
| `insuredcontactphone_encryption` | varchar(200) |  |  |  |  |  |
| `insuredaddress_encryption` | varchar(200) |  |  |  |  |  |
| `cAgency` | varchar(500) |  |  | 否 | '' |  |
| `cTenderer_address` | varchar(500) |  |  | 否 | '' |  |
| `cProjectNo_encryption` | varchar(500) |  |  | 否 | '' |  |
| `cProjectName_encryption` | varchar(1000) |  |  |  | '' |  |
| `cProjectArea_encryption` | varchar(500) |  |  | 否 | '' |  |
| `fFender_expire` | int |  |  | 否 | 0 |  |
| `cContactIDNo` | varchar(50) |  |  | 否 | '' |  |
| `cBidFileUrls` | varchar(1000) |  |  | 否 | '' |  |
| `tender_type` | nvarchar(30) |  |  | 否 | '' |  |
| `fCoInsuranceState` | tinyint |  |  | 否 | 0 |  |
| `CheckTime` | datetime |  |  |  |  |  |
| `third_UUID` | varchar(50) |  |  |  |  |  |
| `fMainCo` | tinyint |  |  | 否 | 0 |  |

## T_PProductYz_Guarantee

*医责险-保单表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cPolicyNo` | varchar(50) |  |  |  |  | 保单号 |
| `cPolicyUrl` | varchar(300) |  |  |  |  |  |
| `tGuaranteedTime_begin` | datetime |  |  |  |  | 保险期限 |
| `tGuaranteedTime_end` | datetime |  |  |  |  | 保险期限 |
| `fEnterpriseInfoID` | int |  |  |  | 0 | 投保人id |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 投保人名称 |
| `fGroupID` | int |  |  |  | 0 | 所属共保体id |
| `cGroupName` | nvarchar(50) |  |  |  |  | 所属共保体名称 |
| `tCreateDate` | datetime |  |  |  | getdate() | 创建时间 |
| `tLastModifyDate` | datetime |  |  |  |  | 最后修改时间 |
| `cUserName` | nvarchar(50) |  |  |  |  | 保单录入人 |
| `fPrcId` | int |  |  |  |  |  |
| `instname` | nvarchar(50) |  |  |  |  | 承保机构 |
| `platformcode` | nvarchar(50) |  |  |  |  | T_PProductYZ_PRCEnInsurance 表 cCode |

## T_PaymentSystem_Enterprise

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cNumber` | varchar(50) |  |  |  |  | 业务平台编号 |
| `cEnterpriseNameCode` | varchar(32) |  |  |  |  | 企业代码 |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 企业名称 |
| `cBank` | varchar(100) |  |  |  |  | 基本户开户行 |
| `cBankCardNo` | varchar(50) |  |  |  |  | 基本户账号 |
| `tUpdateTime` | datetime |  |  |  |  | 更新时间 |

## T_XK_Contacts

*线客联系人表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cType` | varchar(50) |  |  |  |  | 规则名称 |
| `cRule` | varchar(500) |  |  |  |  | 预警规则JSON形式存放 |

## T_PProduct_Guarantee

*农民工履约保单表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cNewGuid` | varchar(50) | 是 |  | 否 |  | 关联履约报单表唯一标识 |
| `tEsignTime` | datetime |  |  |  |  | 签章时间 |
| `tPushTimeToUW` | datetime |  |  |  |  | 提交核保时间 |
| `fIsUnderWriting` | tinyint |  |  |  | 0 | 核保状态，默认0无，4待核保，6核保通过，9核保驳回 |
| `tUnderWritingTime` | datetime |  |  |  |  | 核保（审核、驳回）时间 |
| `cUnderWritingOpinion` | nvarchar(300) |  |  |  |  | 核保意见 |
| `cPaymentMethod` | nvarchar(30) |  |  |  |  | 支付方式（作废） |
| `tPayTime` | datetime |  |  |  |  | 支付时间 |
| `cPaymentType` | nvarchar(30) |  |  |  |  | 支付类型 |
| `cSourceCode` | varchar(50) |  |  |  |  | 业务推荐码 |
| `cBankCardNo` | varchar(50) |  |  |  |  | 基本户 |
| `fInvoiceType` | tinyint |  |  | 否 | 0 | 发票先选发票类型值 承保平台配置发票先选才有意义： 0 普票 2 专票 |
| `tGuaranteedTime` | datetime |  |  |  |  | 出单时间 |
| `fIsGuaranteed` | tinyint |  |  |  | 0 | 出单状态，默认0无，4待出单，6已出单 |
| `cInsuranceTypeNo` | varchar(50) |  |  |  |  | 险种编码 |
| `cPRCCode` | nvarchar(50) |  |  |  |  | 承保机构编码 |
| `cOrganName` | nvarchar(50) |  |  |  |  | 承保机构简称 |
| `cPaymentSerialNumber` | varchar(10) |  |  |  |  | 打款序列号 |
| `fEsignState` | tinyint |  |  | 否 | 0 | 签章状态 0 默认 1 待签章 4 已签章，5无需签章 |
| `cToEsignUrl` | varchar(200) |  |  |  |  | 待签章文件 |
| `tStartTime` | datetime |  |  |  |  | 投保须知打开时间 |
| `tEndTime` | datetime |  |  |  |  | 投保须知查看完成时间 |
| `cCode` | nvarchar(50) |  |  |  |  | 险种方案编码 |
| `fComputeMode` | int |  |  |  | 2 | 保费计算模式 1区间费率 2固定费率 3人工 |
| `fDockingMode` | tinyint |  |  |  | 1 | 对接模式  1保司接口出单 2线下人工出单，3线下出单，代出保单 |
| `fInvoiceCategory` | tinyint |  |  | 否 | 0 | 发票类型（0：增值税普通发票（电子发票）；2：增值税专用发票（纸质发票，邮寄送达邮费到付）） |
| `cDirectorname` | nvarchar(50) |  |  |  |  | 监管单位名称 |
| `cContactUserName` | nvarchar(50) |  |  |  |  | 被保险人联系人 |
| `cContactUserTel` | nvarchar(50) |  |  |  |  | 被保险人联系方式 |
| `cOwnerSheng` | varchar(10) |  |  |  |  | 被保险人省 |
| `cOwnerShi` | varchar(10) |  |  |  |  | 被保险人市 |
| `cOwnerQu` | varchar(10) |  |  |  |  | 被保险人区 |
| `cOwnerNature` | varchar(10) |  |  |  |  | 被保险企业性质 |
| `cAccessKey` | nvarchar(200) |  |  |  |  | 联银担保第三方推送URL地址 |
| `cZipUrl` | varchar(100) |  |  |  |  | 投保附件打包文件 |
| `fIsRejectnotice` | tinyint |  |  |  | 0 | 中心缴存状态通知接口，默认0无，1人社驳回（可退保、可批改），3缴存取消或申请退保（人社驳回后企业取消该缴存方式）（可退保），6, 缴存成功 |
| `tRejectnoticeTime` | datetime |  |  |  |  | 中心缴存驳回通知时间（申请退保时间） |
| `fIsPolicyFiling` | tinyint |  |  | 否 | 0 | 归档状态，默认0无，6已归档， |
| `fPremiumMode` | tinyint |  |  |  |  | 保费计算类型 1直接计算保费（先签章后审核） 2后置展示保费（先审核后签章） |
| `cFirmUUID` | varchar(50) |  |  |  |  | 影像uuid |
| `fPolicyType` | tinyint |  |  |  | 0 | 保单类型 1保单附凭证 2仅保单 3保单凭证各一份 |
| `cPolicyPzUrl` | varchar(500) |  |  |  |  | 保单凭证 |
| `cPostalCode` | varchar(50) |  |  |  |  | 投保人邮政编码 |
| `cBeneficiary` | nvarchar(50) |  |  |  |  | 受益人 |
| `cConstructionType` | nvarchar(30) |  |  |  |  | 最高建筑施工资质类型 |
| `cConstructionGrade` | nvarchar(30) |  |  |  |  | 最高建筑施工资质等级 |
| `fBusinessAmountType` | tinyint |  |  |  |  | 营业规模   1：营业收入>=8亿元；  2：6000万=<营业收入<8亿；   3：营业收入<6000万 |
| `fCompanyAmountType` | tinyint |  |  |  |  | 资产规模  1： 资产规模>=8亿元；  2：5000万=<资产规模<8亿；   3：资产规模<5000万 |
| `fApplyType` | int |  |  | 否 | 0 | 申请类型 1新保 2续保 3补缴 |
| `fApplyClaimAmount` | decimal(18,2) |  |  | 否 | 0 |  |
| `fRegulatorId` | int |  |  | 否 | 0 | 监管单位id |
| `fApplyPush` | int |  |  | 否 | 0 | 履约保函申请结果通知（0：未通知；1：已通知；） |
| `tApplyPushTime` | datetime |  |  |  |  | 履约保函申请结果通知时间 |
| `fIsInvalid` | tinyint |  |  | 否 | 0 | 失效状态，默认0否，1是 |
| `cQuitReason` | nvarchar(1000) |  |  |  |  | 申请退保原因 |
| `cContractFileUrl` | nvarchar(1000) |  |  |  |  | 合同文件 |
| `fHetongDays` | int |  |  | 否 | 0 | 合同期限 |
| `cRenewalOrder` | nvarchar(100) |  |  |  |  | 历史保单号 |
| `cContractFileName` | nvarchar(100) |  |  |  |  |  |
| `cRenewalPolicy` | varchar(100) |  |  |  |  |  |
| `ErrorInfo` | varchar(100) |  |  |  |  | 记录人保山西农民工异常信息 |
| `fMessageState` | int |  |  | 否 | 0 | 核保以及投保单号短信通知  0：未处理   1:投保通知发送成功 2:投保通知发送失败   3:核保通知发送成功 4:核保通知发送失败 |
| `cLocalPolicyUrl` | varchar(200) |  |  |  |  | 本地保单查询地址 |
| `cLocalPolicyPzUrl` | varchar(200) |  |  |  |  | 本地凭证查询地址 |
| `fEstimateRate` | decimal(10,3) |  |  |  |  | 预估费率 |
| `fEstimatePremium` | decimal(18,2) |  |  |  |  | 预估保费 |
| `fMoneyFrom` | tinyint |  |  |  |  | 项目资金来源(1:财政资金；2:企业自筹（银行信贷/机构投资/发行债券/租赁融资）) |
| `fAssets` | decimal(18,2) |  |  |  |  | 上一年度总资产（元） |
| `fDebt` | decimal(18,2) |  |  |  |  | 上一年度总负债（元） |
| `fDebtRate` | decimal(18,2) |  |  |  |  |  |
| `fIsSignFileAudit` | tinyint |  |  | 否 | 0 | 默认值0不需要签章文件审核，1签章文件待审核，2签章文件审核通过，3签章文件审核驳回 |
| `cSignFileAuditNotes` | nvarchar(100) |  |  |  |  | 签章文件审核意见 |
| `tSignFileAuditTime` | datetime |  |  |  |  | 签章文件审核时间 |
| `fIsMinDate` | tinyint |  |  |  |  | 是否限制最小保期 0不限制 1限制 |
| `fProjectType` | tinyint |  |  |  |  | 项目类型 1新建 2在建 |
| `tRenewalOrderEndTime` | datetime |  |  |  |  | 历史保单终保日期 |
| `tZBDate` | datetime |  |  |  |  | 中标日期 |
| `cPerformNo` | varchar(100) |  |  |  |  | 执行单号 |
| `tGuaranteedTime_limit` | datetime |  |  |  |  | 监管建议保险止期 |
| `cOrderOwner` | varchar(50) |  |  |  |  | 保单归属人 |
| `fMarginAmountHandleType` | int |  |  |  |  | 办理类型（1，项目保证金 2，企业保证金） |
| `ccentralProjectProvinceCode` | varchar(50) |  |  |  |  | 中心端 省编码 |
| `ccentralProjectCityCode` | varchar(50) |  |  |  |  | 中心端 市编码 |
| `ccentralProjectProvince` | varchar(100) |  |  |  |  | 中心端 省 |
| `ccentralProjectCity` | varchar(100) |  |  |  |  | 中心端 市 |
| `ccentralProjectArea` | varchar(100) |  |  |  |  | 中心端 区 |
| `ccentralProjectAreaCode` | varchar(50) |  |  |  |  | 中心端 区编码 |
| `cInsProgrammeName` | nvarchar(50) |  |  |  |  | 保险方案名称 |
| `fcInsProgrammeId` | int |  |  |  |  | 保险方案id |
| `cAccidentDesc` | nvarchar(500) |  |  |  |  | 进3年事故描述 |
| `fDelayApplyId` | int |  |  | 否 | 0 | 延期申请表id |
| `fForcedIssue` | tinyint |  |  | 否 | 0 | 是否强制人工出单，默认0否，1是 |
| `cFileUrl` | nvarchar(300) |  |  |  |  | 内蒙多险种弹框填单页附件 |
| `cPolicyNoPz` | varchar(50) |  |  |  |  | 凭证号 |
| `fIsMorePolicy` | tinyint |  |  | 否 | 0 | 是否多单 0 否 1 是 |
| `tFirstBegin` | datetime |  |  |  |  | 首单保险起期 |
| `fUserType` | int |  |  |  |  | 海南腾龙 同项目编号多次投保 用户类型不同 |
| `cChangeReason` | nvarchar(1000) |  |  |  |  |  |
| `cQuitOrderNo` | varchar(100) |  |  |  |  |  |
| `cQuitUserName` | varchar(100) |  |  |  |  |  |
| `cQuitUserPhone` | varchar(100) |  |  |  |  |  |
| `cOwerSincerityLevel` | varchar(100) |  |  |  |  |  |
| `cConstructionSincerityLevel` | varchar(100) |  |  |  |  |  |
| `tGuaranteedIntentionTimeBegin` | datetime |  |  |  |  |  |
| `tGuaranteedIntentionTimeEnd` | datetime |  |  |  |  |  |
| `fIsTestOrder` | tinyint |  |  | 否 | 0 |  |
| `fBusiId` | int |  |  | 否 | 0 | T_PProduct_PRCEnInsuranceBusiManager 表id |
| `fCheckUnderWriting` | tinyint |  |  |  | 0 | 核保是否复核，0否，1待复核，2已复核 |
| `tCheckUnderWritingTime` | datetime |  |  |  |  | 复核时间 |
| `cCheckUnderWritingOpinion` | nvarchar(300) |  |  |  |  | 核保复核意见 |
| `cBusiTips` | nvarchar(50) |  |  |  |  | 业务需求描述话术(用户填写) |
| `fFillFrom` | tinyint |  |  | 否 | 0 | 多险种填单来源，默认0中心过来，1后台填单（山西） |
| `fDepositType` | tinyint |  |  | 否 | 0 | 缓存类型，默认0无，1按预设比例缴存，3减少保证金应缴金额，5增加保证金应缴金额 |
| `fWarnInsuranceID` | int |  |  | 否 | 0 | 关联T_PProductWarn_Insurance表ID，山西填单用到 |
| `fIsMian` | tinyint |  |  |  | 0 | 是否主账号（0：否；1：是）（山西工资监管项目用） |
| `fAccountType` | tinyint |  |  |  | 0 | 账户类型（1：农民工工资专户；2：保证金账户；3：银行保函；4：工程担保公司保函；5：工程保证保险）（山西工资监管项目用） |
| `cInsuranceFullName` | nvarchar(50) |  |  |  |  | 保险公司全称 |
| `fAccountStatus` | tinyint |  |  |  | 0 | 账户状态  1:待验证,2:已校验,3:校验失败,4:注销,5：挂失,6：冻结,9：其他 |
| `fAccountSpec` | tinyint |  |  |  | 0 | 银行是否对账户设置特殊标识（0：否；1：是） |
| `cBranchName` | nvarchar(30) |  |  |  |  | 支行名称 |
| `fDiDepositAmount` | decimal(18,2) |  |  |  | 0 | 差异化存缴金额 |
| `cQuotationNo` | nvarchar(50) |  |  |  |  | 询价单号 |
| `tInvalidTime` | datetime |  |  |  |  | 失效时间 |
| `fBidderLevel` | tinyint |  |  |  | 0 | 投保企业信用等级 |
| `fPProductProgrammeID` | int |  |  | 否 | 0 | T_PProduct_Programme表id |
| `cChannelName` | varchar(255) |  |  |  |  | 渠道名称 |
| `cChannelCode` | varchar(255) |  |  |  |  | 渠道编码 |
| `cCoAssurer` | nvarchar(100) |  |  |  |  | 共同被保人 |
| `OrderId` | nvarchar(50) |  |  |  |  |  |
| `cSource` | nvarchar(50) |  |  |  |  | 自贡  ：数据来源，传值“企业新增/交易系统同步” |
| `cContent` | nvarchar(2000) |  |  |  |  | 自贡：人社审核意见 |
| `fIsPaidNotice` | int |  |  |  | 0 | 支付结果通知（个别地区需要，默认0 ，0未推送 1已推送） |
| `cGuaranteePurpose` | nvarchar(50) |  |  |  |  | 保函用途 |
| `fpayOnDemand` | int |  |  |  | 0 | 见索即付  （0：否；1：是） 杭州政采-联银用到 |
| `cHGCode` | nvarchar(50) |  |  |  |  |  |
| `cContactUserIDNumber` | nvarchar(50) |  |  |  |  |  |

## T_PProduct_InvoiceLog

*农民工履约保函发票表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  | 0 | 企业表ID |
| `fType` | tinyint |  |  |  |  | 0普票电子发票，1普票纸质发票，2专票纸质发票 |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 企业名称 |
| `cEnterpriseNameCode` | varchar(50) |  |  |  |  | 统一社会信用代码 |
| `cProjectName` | nvarchar(200) |  |  |  |  | 工程名称 |
| `cUser` | nvarchar(20) |  |  |  |  | 联系人 |
| `cUserPhone` | varchar(50) |  |  |  |  | 联系人手机 |
| `cAddress` | nvarchar(50) |  |  |  |  | 发票邮寄地址 |
| `cEmail` | nvarchar(40) |  |  |  |  | 电子邮箱 |
| `cBank` | nvarchar(30) |  |  |  |  | 开户行 |
| `cAccount` | nvarchar(30) |  |  |  |  | 开户账号 |
| `fGuaranteeInfoID` | int |  |  |  | 0 | 保单表ID |
| `fProjectID` | int |  |  |  | 0 | 项目表ID |
| `fInvoiceAmount` | numeric(18,2) |  |  |  | 0 | 发票金额 |
| `fState` | tinyint |  |  | 否 | 0 | 状态：0申请(用户向我方申请开票)，1 提交中(向保险公司申请开票) 2提交(保险公司开票成功)，3已推送，4推送失败，9自动生成一条 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |
| `tAppTime` | datetime |  |  |  |  | 用户申请时间 |
| `tSubTime` | datetime |  |  |  |  | 开票时间 |
| `invoiceUrl` | varchar(200) |  |  |  |  | 电子发票下载地址 |
| `invoiceCode` | varchar(50) |  |  |  |  | 发票代码 |
| `invoiceNo` | varchar(50) |  |  |  |  | 发票号码 |
| `ErrMsg` | nvarchar(200) |  |  |  |  | 在线开票失败原因 |
| `platformCode` | varchar(50) |  |  |  |  |  |
| `cTel` | varchar(20) |  |  |  |  | 税务登记联系电话 |
| `cCompanyAddress` | nvarchar(100) |  |  |  |  | 税务登记地址 |
| `fZt` | tinyint |  |  |  | 0 | 新履约开票状态，默认0无，4待开票，6已开票，7只申请，不处理（深圳农民工用到） |
| `cExpressNo` | varchar(50) |  |  |  |  | 快递单号 |
| `fSourceType` | tinyint |  |  | 否 | 0 | 数据来源 2多险种履约平台 |
| `signInvoice` | varchar(200) |  |  |  |  | 确认函文件 |
| `cRemarks` | nvarchar(100) |  |  |  |  | 备注 |

## T_PProduct_ProductCompany

*项目三方责任人信息*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cCompanyName` | nvarchar(50) |  |  |  |  | 企业名称 |
| `cCompanyCode` | varchar(50) |  |  |  |  | 统一社会信用代码 |
| `cCompanyNature` | nvarchar(20) |  |  |  |  | 单位性质 |
| `cContactUserName` | nvarchar(100) |  |  |  |  | 联系人姓名 |
| `cContactUserPhone` | nvarchar(100) |  |  |  |  | 联系人电话 |
| `fType` | tinyint |  |  |  |  | 类型（1：施工单位（总包）；2：建设单位；3：监理单位；4：施工单位（分包）） |
| `tCreateDate` | datetime |  |  |  | getdate() | 创建时间 |
| `cAddress` | nvarchar(100) |  |  |  |  | 地址 |
| `fProductInfoId` | int |  |  |  |  | 项目表id |
| `fConstructType` | tinyint |  |  |  |  | 施工单位 类型   1 总包 2 分包---字段作废 |

## T_Base_PostCode

*地区邮编表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cAreaCode` | varchar(10) |  |  | 否 |  | 地区编码 |
| `cPostCode` | varchar(10) |  |  | 否 |  | 地区邮编 |
| `id` | int | 是 | 是 | 否 |  |  |

## T_QuitGuarantee_GuaranteeAttachment

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(64) |  |  | 否 |  |  |
| `fAttachmentID` | int |  |  | 否 | 0 |  |
| `cCode` | varchar(200) |  |  | 否 |  |  |
| `fPRCEnInsuranceEnAttachmentID` | int |  |  | 否 | 0 |  |
| `cLocalUrl` | varchar(200) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_PaymentSystem_Guarantee

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cNumber` | varchar(50) |  |  |  |  | 业务平台编号 |
| `cInsuranceCompany` | nvarchar(50) |  |  |  |  | 保险公司 |
| `cPolicyNo` | nvarchar(50) |  |  |  |  | 保单号 |
| `fPremium` | decimal(18,2) |  |  |  | 0 | 保费金额 |
| `cEnterpriseNameCode` | nvarchar(32) |  |  |  |  | 投保企业代码 |
| `cEnterpriseName` | nvarchar(20) |  |  |  |  | 投保企业名称 |
| `fOrderId` | int |  |  |  |  | 订单id |
| `cOrderNo` | varchar(50) |  |  |  |  | 订单号 |
| `cTransNo` | varchar(50) |  |  |  |  | 银行流水号 |
| `tGuaranteedTime` | datetime |  |  |  |  | 出函时间 |
| `fState` | tinyint |  |  |  | 0 | 是否退保 0 未退保 1 已退保 |

## T_GzZrx_PRCInsType

*雇主责任险--二级渠道和险种关联表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCID` | int |  |  | 否 | 0 | T_GzZrx_PRC二级渠道表id |
| `fInsuranceTypeID` | int |  |  | 否 | 0 | T_GzZrx_Insurance险种表id |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |
| `fBalanceMode` | tinyint |  |  | 否 | 0 | 是否启用余额模式 0 否 1 是 |

## T_OnlineInvoice_QueryLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fUserID` | int |  |  |  |  |  |
| `IpAddress` | varchar(20) |  |  |  |  | IP地址 |
| `OptType` | tinyint |  |  |  |  | 操作类型 1 登录， 2查询-1， 3查询-2 |
| `Params` | nvarchar(1000) |  |  |  |  | 相关参数 |
| `IsValidQuery` | bit |  |  | 否 | 0 | 是否有效搜索 0否 1是 |
| `CreateTime` | datetime |  |  | 否 | getdate() | 操作时间 |
| `DataSource` | tinyint |  |  | 否 | 1 | 数据源 1核心库 2省平台 |

## T_Base_User

*投保联系人信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `cRealName` | nvarchar(50) |  |  |  |  | 姓名 |
| `cPhone` | varchar(50) |  |  |  |  | 手机 |
| `cEmail` | varchar(50) |  |  |  |  | 邮箱 |
| `cAddress` | nvarchar(100) |  |  |  |  | 地址 |
| `CreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `fIsDelete` | bit |  |  | 否 | 0 | 是否删除 |
| `fIsDefault` | bit |  |  | 否 | 0 |  |
| `cCompanyAddress` | nvarchar(100) |  |  |  |  |  |

## T_QuitGuarantee_Manual

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  |  |  |  |
| `cPolicyNo` | nvarchar(50) |  |  |  |  |  |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  |  |
| `cRealName` | nvarchar(50) |  |  |  |  |  |
| `cPhone` | nvarchar(50) |  |  |  |  |  |
| `tPolicyTime` | datetime |  |  |  |  |  |
| `tQuitApplyTime` | datetime |  |  | 否 | getdate() |  |
| `fState` | int |  |  | 否 | 0 |  |
| `quitIsPush` | int |  |  | 否 | 0 |  |
| `fQuitState` | tinyint |  |  | 否 | 0 |  |
| `cAuditUserName` | nvarchar(50) |  |  |  |  |  |
| `cReason` | nvarchar(200) |  |  |  |  |  |
| `cFileUrls` | varchar(200) |  |  |  |  |  |
| `platformcode` | varchar(50) |  |  |  |  |  |
| `fPayId` | int |  |  |  |  |  |
| `fIsTest` | tinyint |  |  | 否 | 0 |  |
| `Prc_Type` | tinyint |  |  | 否 | 0 |  |
| `cRemark` | nvarchar(100) |  |  |  | NULL |  |
| `cLicenseLocalUrl` | varchar(100) |  |  |  | NULL |  |
| `cAccountCertLocalUrl` | varchar(100) |  |  |  | NULL |  |
| `cBiddingDocLocalUrl` | varchar(100) |  |  |  | NULL |  |
| `cCorporationIDCardLocalUrl` | varchar(100) |  |  |  | NULL |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |
| `cToQuitEsignUrl` | varchar(200) |  |  |  | NULL |  |
| `cQuitEsignUrl` | varchar(200) |  |  |  | NULL |  |
| `cToQuitAccountEsignUrl` | varchar(200) |  |  |  | NULL |  |
| `cQuitAccountEsignUrl` | varchar(200) |  |  |  | NULL |  |
| `tQuitEsignTime` | datetime |  |  |  | NULL |  |
| `tQuitFinishTime` | datetime |  |  |  | NULL |  |
| `fQuitFrom` | tinyint |  |  | 否 | 2 |  |
| `fIsTkType` | tinyint |  |  | 否 | 1 | 0保司退保退款，1已退保退款 |
| `fIsTk` | tinyint |  |  | 否 | 0 | 0未退款，1已退款 |
| `cBlrName` | nvarchar(20) |  |  |  |  | 退保办理人 |
| `cBlrPhone` | varchar(20) |  |  |  |  | 退保办理人手机号 |

## T_GzZrx_Users

*雇主责任险-用户表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Id` | varchar(50) | 是 |  | 否 |  |  |
| `cPassword` | nvarchar(50) |  |  | 否 |  | 登录密码 |
| `cTelePhone` | varchar(50) |  |  | 否 |  | 手机号 |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 企业名称 |
| `cEnterpriseNameCode` | varchar(50) |  |  |  |  |  |
| `cJob` | nvarchar(50) |  |  |  |  | 工作岗位 |
| `cRealName` | nvarchar(50) |  |  | 否 |  | 真实姓名 |
| `IsDeleted` | bit |  |  | 否 |  | 删除状态，true是，false否 |
| `IsDisable` | bit |  |  | 否 |  | 禁用状态，true是，false否 |
| `fFrom` | tinyint |  |  |  | 0 | 创建来源，0后台创建，1渠道管理员创建 |
| `cFromId` | varchar(50) |  |  |  |  | 对应渠道fFrom=1时，渠道管理员ID |
| `cRemark` | nvarchar(500) |  |  |  |  | 备注说明 |
| `cRolesTypeCode` | varchar(20) |  |  |  |  | 角色类型，对应T_GzZrx_RolesType表cTypeCode |
| `tCreateTime` | datetime |  |  | 否 |  | 创建时间 |
| `tUpdateTime` | datetime |  |  |  |  | 账号修改时间 |
| `tLoginTime` | datetime |  |  |  |  | 最近登录时间 |
| `fTag` | tinyint |  |  |  | 0 | 默认0传化责任险 |
| `cRolesID` | varchar(50) |  |  |  |  | 角色ID，关联T_GzZrx_Roles表ID |
| `cDataPermissionsID` | varchar(50) |  |  |  |  | 数据权限ID，关联T_GzZrx_DataPermissions表ID |
| `fLoginErrCount` | int |  |  |  |  | 登录错误次数 |
| `cParentUserId` | varchar(50) |  |  |  |  | 父级UserId，关联表Users表本身 |
| `tUpdateUserId` | varchar(50) |  |  |  |  | 上一次修改信息的人 |
| `tUpdateUserName` | nvarchar(50) |  |  |  |  | 上一次修改信息的人 |
| `fAvailableAmount` | decimal(10,2) |  |  | 否 | 0 | 可用余额 |
| `fGuaranteeCount` | int |  |  | 否 | 0 | 使用余额支付的订单数 |
| `platformcode` | varchar(50) |  |  |  |  |  |
| `cServiceInsuranceTypeNo` | varchar(100) |  |  |  |  | 支持险种编码，多个以逗号,隔开 |

## T_PaymentSystem_PayLog

*支付记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `transno` | varchar(50) | 是 |  | 否 |  | 银行流水号 |
| `transtime` | datetime |  |  | 否 |  | 支付时间 |
| `transamount` | decimal(18,2) |  |  | 否 |  | 支付金额 |
| `payeracctno` | varchar(50) |  |  | 否 |  | 付款卡号 |
| `payeracctname` | nvarchar(100) |  |  | 否 |  | 付款户名 |
| `abstractinfo` | nvarchar(100) |  |  |  |  | 备注 |
| `oppositebankno` | varchar(50) |  |  | 否 |  | 付款行号 |
| `oppositebankname` | nvarchar(50) |  |  | 否 |  | 付款行名 |
| `tdate` | datetime |  |  | 否 | getdate() | 日期 |
| `OrderNo` | varchar(50) |  |  |  |  | 打款序列号 |
| `fState` | tinyint |  |  | 否 | 0 | 0:未使用，1：已使用，2：退款中，3：已退款 |
| `fisPush` | tinyint |  |  | 否 | 0 | 0：未推送，1：已推送 |
| `tPushTime` | datetime |  |  |  |  | 推送时间 |
| `fOrderID` | int |  |  |  |  | 订单ID |
| `ResultCode` | tinyint |  |  |  |  | 支付结果，0：成功，1：基本户校验错误，2：支付金额校验错误，3：无该用户代收代付需求 |
| `TimeStab` | varchar(50) |  |  |  |  |  |
| `transtdate` | date |  |  |  |  |  |
| `skAccount` | varchar(50) |  |  |  |  |  |
| `cardType` | tinyint |  |  |  |  |  |
| `cAuditMessage` | nvarchar(100) |  |  |  |  |  |
| `cAuditUserName` | nvarchar(50) |  |  |  |  |  |
| `cAuditTime` | datetime |  |  |  |  |  |
| `fState_tk` | tinyint |  |  | 否 | 0 | 该字段当fState等于3时有效，退款类别说明，默认0未出函退款，2退保退款，3：注销退款，4：保司退保退款（3,4两种状态是2的细分） |
| `fPushCount` | int |  |  | 否 | 0 |  |
| `ftkIsPush` | tinyint |  |  | 否 | 0 | 未出函退款推送 0 未推送 1 已推送 |

## T_GzZrx_InvoiceInfo

*履约企业发票信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `fType` | tinyint |  |  |  | 0 | 0普票电子发票，1普票纸质发票，2专票纸质发票 |
| `cUser` | nvarchar(20) |  |  |  |  | 联系人 |
| `cUserPhone` | varchar(50) |  |  |  |  | 税务登记电话 |
| `cAddress` | nvarchar(50) |  |  |  |  | 税务登记地址 |
| `cEmail` | nvarchar(40) |  |  |  |  | 电子邮箱 |
| `cTel` | varchar(50) |  |  |  |  | 联系人手机号 |
| `cBank` | nvarchar(30) |  |  |  |  | 开户行 |
| `cAccount` | nvarchar(30) |  |  |  |  | 开户账号 |
| `CreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `cCompanyAddress` | nvarchar(100) |  |  |  |  | 收件地址 |
| `SignInvoice` | varchar(200) |  |  |  | '' | 专票提醒确认函 |
| `isSignInvoice` | tinyint |  |  |  | 0 | 是否已签章，0：否，1：是 |
| `cTaxPayerNo` | varchar(50) |  |  |  |  | 纳税人识别号 |
| `cTaxPayerFile` | varchar(200) |  |  |  |  | 纳税证明文件 |

## T_PProduct_ProductInfoExtend

*农民工项目扩展表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fProjectID` | int |  |  |  | 0 | 关联T_PProduct_ProductInfo表ID |
| `fClaimsCount` | int |  |  |  | 0 | 理赔总数 |
| `fServeCount` | int |  |  |  | 0 | 服务总数 |
| `fServeOKCount` | int |  |  |  | 0 | 服务完成总数 |
| `fRisk_SeriousCount` | int |  |  |  | 0 | 重大危险次数 |
| `fRisk_GeneralCount` | int |  |  |  | 0 | 一般危险次数 |
| `fRisk_SlightCount` | int |  |  |  | 0 | 重大危险次数 |
| `fRisk_RetentionCount` | int |  |  |  | 0 | 保留风险 |
| `fRectifyCount` | int |  |  |  | 0 | 整改总销项 |
| `fRectifyOKCount` | int |  |  |  | 0 | 整改完成销项 |
| `CreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `fClaimsOKCount` | int |  |  |  | 0 | 理赔完成总数 |
| `fRiskOKCount` | int |  |  |  | 0 | 风险完成数量 |

## T_Black_WuXi

*无锡投保黑名单*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 企业名称 |
| `cEnterpriseNameCode` | varchar(50) | 是 |  | 否 |  | 统一社会编码 |
| `cType` | nvarchar(50) | 是 |  | 否 |  | 资质类型 |
| `cGrade` | nvarchar(10) | 是 |  | 否 |  | 资质等级 |
| `fScore` | decimal(10,2) |  |  | 否 |  | 总评分 |
| `tdate` | datetime |  |  |  | getdate() | 创建日期 |
| `lastdate` | datetime |  |  |  | getdate() | 最后修改日期 |

## T_Pay_Log_Interface

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  | 否 |  | 订单表cNewGuid |
| `outTradeNo` | varchar(50) | 是 |  | 否 |  | 支付流水号 |
| `payAmount` | decimal(18,2) |  |  | 否 |  | 支付金额 |
| `goodsName` | nvarchar(20) |  |  | 否 |  | 商品名称 |
| `goodsBody` | nvarchar(100) |  |  |  |  | 商品描述 |
| `codeUrl` | varchar(200) |  |  |  |  | 二维码链接 |
| `expireTime` | datetime |  |  | 否 |  | 链接有效期 |
| `insuranceName` | nvarchar(10) |  |  |  |  | 保司名称 |
| `fState` | tinyint |  |  | 否 | 0 | 支付状态 0 默认 1 成功 |
| `serialNo` | int |  |  | 否 | 0 |  |
| `payTime` | datetime2 |  |  |  |  | 支付时间 |
| `payType` | nvarchar(50) |  |  |  |  | 支付类型 |
| `isBatch` | tinyint |  |  | 否 | 0 |  |
| `transactionId` | varchar(50) |  |  |  |  | 微信支付号 |
| `lastUpdatetime` | datetime |  |  |  |  | 上一次更新时间 |

## T_PaymentSystem_Platform

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cNumber` | varchar(50) | 是 |  | 否 |  | 业务平台编号 |
| `cPlatformNumber` | varchar(50) |  |  |  |  | 主平台编号 |
| `cInsuranceNumber` | varchar(50) |  |  |  |  | 保险公司编号 |
| `cOrgName` | nvarchar(50) |  |  |  |  | 承保机构名称 |
| `cBank` | nvarchar(50) |  |  |  |  | 收款开户行 |
| `cUserName` | nvarchar(50) |  |  |  |  | 收款账户名称 |
| `cAccount` | varchar(50) |  |  |  |  | 收款账号 |
| `cRemarks` | nvarchar(100) |  |  |  |  | 备注 |
| `cProvince` | nvarchar(30) |  |  |  |  | 省 |
| `cCity` | nvarchar(30) |  |  |  |  | 市 |
| `cArea` | nvarchar(30) |  |  |  |  | 区 |
| `CreateTime` | datetime |  |  |  | getdate() |  |
| `pushUrl` | varchar(200) |  |  |  |  |  |
| `payPage` | varchar(200) |  |  |  |  |  |
| `MinfPremium` | decimal(10,2) |  |  |  |  |  |
| `fRate` | decimal(10,2) |  |  |  |  |  |
| `dataapiurl` | varchar(200) |  |  |  |  |  |
| `cBlackCheckUrl` | varchar(200) |  |  |  |  |  |
| `cLocalBlackCheckUrl` | nvarchar(200) |  |  |  |  | 内部平台黑名单验证接口 |
| `fIsRecipient` | tinyint |  |  | 否 | 1 | 是否中惠代收（1：是；0：否）  这个参数会影响【退款事项处理】功能流程 |
| `fIsPushErrorState` | tinyint |  |  | 否 | 0 |  |
| `fXKPlatformId` | int |  |  | 否 | 0 |  |
| `fRunState` | tinyint |  |  |  | 0 |  |
| `id` | int |  | 是 | 否 |  |  |
| `cMaualCity` | nvarchar(50) |  |  |  |  |  |
| `cMaualArea` | nvarchar(50) |  |  |  |  |  |

## T_PProduct_ProductSecurityOfficer

*安全员信息*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fProductInfoId` | int |  |  |  |  | 项目表id |
| `cName` | nvarchar(50) |  |  |  |  | 姓名 |
| `cTitle` | nvarchar(50) |  |  |  |  | 职位 |
| `cPhone` | varchar(20) |  |  |  |  | 手机号 |

## T_Ca_Log

*CA登录日志表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `CaID` | varchar(50) |  |  |  |  |  |
| `cIP` | varchar(50) |  |  |  |  |  |
| `cMac` | varchar(50) |  |  |  |  |  |
| `cBrowser` | varchar(50) |  |  |  |  |  |
| `CreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `ORes` | tinyint |  |  |  |  |  |
| `ReturnCert` | varchar(MAX) |  |  |  |  | CA登陆返回值 |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `Prc_Code` | varchar(50) |  |  |  |  |  |
| `cInsuranceCode` | varchar(50) |  |  |  |  |  |

## T_QuotaProject

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fProjectID` | int |  |  |  |  |  |

## T_PaymentSystem_Vouchers

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `OrderId` | int |  |  | 否 |  |  |
| `cPaymentSerialNumber` | varchar(4) |  |  | 否 |  | 打款序列号 |
| `cPaymentVoucher` | varchar(100) |  |  | 否 |  | 图片地址 |
| `tPaymentVoucherTime` | datetime |  |  | 否 |  | 上传时间 |
| `fIsSend` | tinyint |  |  | 否 | 0 |  |

## T_PProduct_Programme

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fInsuranceID` | int |  |  | 否 |  | T_PProduct_Insuranceinfo表ID |
| `fInsuranceTypeID` | int |  |  | 否 |  | T_PProduct_Insurance表ID |
| `fPRCID` | int |  |  | 否 |  | T_PProduct_PRC表ID |
| `cName` | varchar(50) |  |  |  |  | 方案名称 |
| `cCode` | varchar(50) |  |  | 否 |  | 方案编码 |
| `cPara` | varchar(500) |  |  |  |  | 方案参数 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cLastEditUser` | nvarchar(50) |  |  |  |  | 最后修改人 |
| `tLastEditTime` | datetime |  |  |  |  | 最后修改时间 |
| `fInsuranceBegin` | int |  |  |  |  | 保期起始天数 |
| `fInsuranceEnd` | int |  |  |  |  | 保期结束天数 |
| `fState` | int |  |  |  |  | 状态 1启用 0停用 |
| `fType` | int |  |  |  |  | 保费计算类型 1按天 2按月 3按年 |
| `fRoundingMode` | int |  |  |  |  | 取整模式 1向上 2向下 3不处理 |
| `fPRCEnInsuranceID` | int |  |  |  |  | 对应T_PProduct_PRCEnInsurance表ID |
| `MinfPremium` | decimal(10,2) |  |  | 否 | 500 | 最低收费 |
| `MaxAmount` | decimal(18,2) |  |  | 否 | 800000 | 最高保额 |
| `StartDate` | tinyint |  |  |  |  |  |
| `StartHour` | tinyint |  |  |  |  |  |
| `fRateType` | tinyint |  |  | 否 | 1 | 费率类型（1：固定费率，2：年费率（绍兴模式）3：年费率（杭州政采，不足30天按30天算） |

## T_CA_Parameter

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `CaID` | varchar(50) | 是 |  | 否 |  |  |
| `srcData` | varchar(50) |  |  | 否 |  |  |
| `signData` | varchar(500) |  |  |  |  |  |
| `certData` | varchar(2500) |  |  |  |  |  |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  |  |
| `platformcode` | varchar(50) | 是 |  | 否 |  |  |

## T_PProduct_Admin

*农民工管理账号*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Id` | varchar(50) | 是 |  | 否 |  |  |
| `fDepartID` | int |  |  |  | 0 |  |
| `cRealName` | nvarchar(10) |  |  |  |  | 账号管理员真实姓名 |
| `cEmail` | varchar(50) |  |  |  |  | 电子邮箱 |
| `cPhone` | varchar(50) |  |  |  |  | 手机号 |
| `Password` | varchar(50) |  |  |  |  | 密码 |
| `fState` | tinyint |  |  |  | 0 | 账号状态，0正常，1禁用，2删除 |
| `fType` | tinyint |  |  |  | 0 | 账号类型，0人设管理员，1部门，2金融机构，3网点 |
| `CreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `LastLoginCount` | int |  |  |  | 0 |  |
| `LastLoginTime` | datetime |  |  |  |  |  |
| `platformCode` | varchar(50) |  |  |  |  | 平台代码 |
| `cUserID` | varchar(50) |  |  |  |  | 录入的用户ID，对应T_PProduct_Admin表ID |

## T_Enterprise_Black

*黑名单拦截企业表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fGuaranteeID` | int |  |  |  | 0 | 关联T_Guarantee_Info表ID |
| `fBlackPRCID` | int |  |  |  | 0 |  |
| `fDisableType` | tinyint |  |  |  | 0 | 冗余字段，禁用类型，默认0永久，1短期 |
| `tEndTime` | datetime |  |  |  |  | 冗余字段，禁用止期 |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `cInsuranceCompany` | varchar(50) |  |  |  |  | 冗余字段，承保机构 |
| `platformcode` | varchar(50) |  |  |  |  | 冗余字段，平台码 |

## T_Region

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Id` | int |  | 是 | 否 |  | 自增Id |
| `RegionName` | nvarchar(50) |  |  | 否 |  | 地区名字 |
| `ParentId` | int |  |  | 否 |  | 父级Id |
| `OrderId` | int |  |  | 否 |  | 排序字段 |

## T_GzZrx_Roles

*雇主责任险-角色表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Id` | varchar(50) | 是 |  | 否 |  |  |
| `CreateDateTime` | datetime |  |  | 否 |  | 创建时间 |
| `Description` | nvarchar(50) |  |  | 否 |  | 备注说明 |
| `IsDeleted` | bit |  |  | 否 |  | 删除状态，true是，false否 |
| `IsSuperRole` | bit |  |  | 否 |  | 是否超级管理员，true是，false否 |
| `Name` | nvarchar(20) |  |  | 否 |  | 名称 |
| `fTag` | tinyint |  |  |  | 0 | 默认0传化责任险 |
| `cTypeCode` | varchar(50) |  |  |  |  | 渠道类型编码，关联T_GzZrx_RolesType表cTypeCode |

## T_DaPingMu_Log

*大屏幕日志*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cEvents` | varchar(10) |  |  |  |  |  |
| `prc_type` | int |  |  |  | 0 | 0核心，1擎州，2温州，3平阳，4福建省宁德市市本级，5安徽省滁州市市本级，6浙江省平台，7佛山内网，99基本户 |
| `fGuaranteeInfoID` | int |  |  |  | 0 | 保单表ID |
| `typeName` | nvarchar(10) |  |  |  |  | 正常、异常 |
| `paramName` | nvarchar(10) |  |  |  |  | 程序名，中文类别 |
| `city` | nvarchar(30) |  |  |  |  | 城市地区 |
| `errMsg` | nvarchar(3000) |  |  |  |  | 错误信息 |
| `createTime` | datetime |  |  |  | getdate() | 创建时间 |
| `updateTime` | datetime |  |  |  |  |  |
| `fstate` | tinyint |  |  |  | 0 | 状态，0未处理，1已处理 |
| `cTag` | varchar(50) |  |  |  |  | 标识唯一值，构成：{events}_{fGuaranteeInfoID}_{prc_type}_{insurance_type} |
| `openIds` | varchar(300) |  |  |  |  |  |
| `openUsers` | nvarchar(50) |  |  |  |  |  |
| `cRemark` | nvarchar(100) |  |  |  |  | 处理备注 |
| `cAuditUserName` | nvarchar(10) |  |  |  |  | 处理人 |
| `tAuditTime` | datetime |  |  |  |  | 处理时间 |
| `insurance_type` | tinyint |  |  |  |  | 默认0是投标订单业务，1多险种订单业务，2投标发票业务，3雇主责任险，4无人机险 |
| `fInvoiceLogID` | int |  |  |  |  |  |
| `tPushDate` | datetime |  |  |  |  | 推送钉钉时间 |
| `fIsPushDing` | tinyint |  |  | 否 | 0 | 是否已推送到钉钉（0：未推送；1：已推送） |
| `fPushType` | tinyint |  |  |  |  | 推送类型，0微信，1钉钉，2(微信和钉钉) |
| `cProblemType` | nvarchar(10) |  |  |  |  |  |

## T_CoInsurance_EmailInfo

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `PRC_id` | int | 是 |  | 否 |  |  |
| `cEmail` | varchar(100) |  |  |  |  |  |
| `tdate` | datetime |  |  | 否 | getdate() |  |

## T_pay_log_discount

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cEnterpriseName` | nvarchar(50) |  |  | 否 |  |  |
| `cEnterpriseNameCode` | varchar(50) |  |  | 否 |  |  |
| `skAccount` | varchar(50) |  |  | 否 |  |  |
| `Discount` | decimal(10,2) |  |  | 否 |  |  |
| `tdate` | datetime |  |  | 否 | getdate() |  |
| `platformcode` | varchar(50) |  |  |  |  | 平台编码 |

## T_Relation_GuaranteeEnAttachment

*投保单和企业附件关联表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `fGuaranteeID` | int |  |  |  |  | 投保单信息表自增ID |
| `fEnterpriseAttachmentID` | int |  |  |  |  | 企业信息附件表自增ID |
| `CreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `fIsPush` | bit |  |  | 否 | 0 |  |

## T_PProduct_Agreement

*多险种合同表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `cInsuranceCompany` | nvarchar(30) |  |  |  |  | 保险公司，比如人保 |
| `platformCode` | varchar(50) |  |  |  |  | 平台编号 |
| `cAgreementNum` | varchar(50) | 是 |  | 否 | (0) | 合同编号 |
| `cAgreementName` | nvarchar(50) |  |  | 否 | (0) | 合同名称 |
| `cServiceOrganizationId` | varchar(50) |  |  |  |  | 服务机构ID， |
| `cService_Organization` | nvarchar(50) |  |  |  |  | 服务机构名称 |
| `cInsuranceFullName` | nvarchar(30) |  |  |  |  | 服务机构全称 |
| `tBeginTime` | datetime |  |  |  |  | 合同起期 |
| `tEndTime` | datetime |  |  |  |  | 合同止期 |
| `cFileUrls` | varchar(200) |  |  |  |  | 合同附件，非必传 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |
| `tUpdateTime` | datetime |  |  |  |  | 最近更新时间 |
| `cNewGuid` | varchar(50) |  |  |  |  | 唯一性标识 |
| `cOpUserID` | varchar(50) |  |  |  |  | 添加人账号ID |
| `cOpUserName` | varchar(50) |  |  |  |  | 添加人账号名称 |

## T_GzZrx_PRCInsuranceEngagedesc

*雇主责任险-特约配置*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCInsuranceID` | int |  |  | 否 | 0 | T_GzZrx_PRCInsurance承保表id |
| `fInsuranceTypeID` | int |  |  | 否 | 0 | 险种id 暂无用 |
| `EngagedescContent` | nvarchar(MAX) |  |  |  |  | 特约内容 |
| `cTitle` | nvarchar(100) |  |  |  |  | 标题 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |
| `cAuditUserName` | nvarchar(20) |  |  |  |  | 创建人 |
| `tUpdateTime` | datetime |  |  | 否 | getdate() |  |
| `fEngagesIsNull` | tinyint |  |  | 否 | 0 |  |

## T_ZX_User

*振鑫小程序用户表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fZXUserID` | int |  |  |  |  | 关联T_ZX_User表ID |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `fType` | tinyint |  |  |  | 0 | 企业类型，0绑定，1添加 |
| `fIsDeleted` | tinyint |  |  | 否 | 0 |  |
| `cInvitationCode` | nvarchar(50) |  |  |  |  | 绑定邀请码 |

## T_PProduct_QualificationRate

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fPRCEnInsuranceID` | int |  |  |  |  | T_PProduct_PRCEnInsurance.ID |
| `fConstructionGradeID` | int |  |  |  |  | T_PProduct_ConstructionGrade.ID |
| `fInsuranceBegin` | int |  |  |  |  | 保期范围起始 (不包含) |
| `fInsuranceEnd` | int |  |  |  |  | 保期范围结束 (包含) |
| `fRate` | decimal(10,4) |  |  |  |  | 费率 |
| `fSort` | int |  |  |  | 0 | 排序 |
| `fMinAmount` | decimal(18,2) |  |  | 否 | 0 |  |
| `fMaxAmount` | decimal(18,2) |  |  | 否 | 99999999999. |  |
| `fProgrammeID` | int |  |  | 否 | 0 | T_PProduct_Programme方案ID |

## T_CoInsurance_Info

*共保分单配置表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `PRC_id` | int |  |  | 否 |  |  |
| `Insurance_id` | int |  |  | 否 |  |  |
| `coinsuranceName` | nvarchar(50) |  |  | 否 |  | 共保机构名称 |
| `ApiUrl` | varchar(250) |  |  | 否 |  | 共保接口地址 |
| `appkey` | varchar(250) |  |  |  |  |  |
| `appsecret` | varchar(50) |  |  | 否 |  |  |
| `tdate` | datetime |  |  | 否 | getdate() |  |
| `fType` | tinyint |  |  | 否 | 0 |  |
| `fispush` | tinyint |  |  | 否 | 0 |  |
| `startday` | date |  |  |  |  |  |
| `fRoleType` | tinyint |  |  | 否 | 0 |  |
| `coinsuranceFullName` | nvarchar(50) |  |  |  |  |  |
| `fPremiumStype` | tinyint |  |  | 否 | 0 |  |
| `Insurance_id_cg` | tinyint |  |  | 否 | 0 |  |
| `appplatformcode` | varchar(20) |  |  |  |  |  |
| `endday` | date |  |  | 否 | '2099-12-31' |  |
| `sm4Key` | varchar(30) |  |  |  |  |  |

## T_GzZrx_WorkType

*雇主责任险-雇员职业类型表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cWorkCode` | varchar(20) |  |  | 否 |  | 职业代码 |
| `cWorkName` | nvarchar(30) |  |  |  |  | 职业名称 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_PProduct_PRCEnInsurance

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(50) |  |  | 否 |  | 客户经理 |
| `fPRCEnInsuranceID` | int |  |  | 否 |  | T_PProduct_PRCEnInsurance 表id |
| `tCreateDate` | datetime |  |  |  | getdate() |  |

## T_Relation_InvoiceSpecSignInfo

*专票确认关系表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `fPRCEnInsuranceID` | int | 是 |  | 否 |  | 承保机构ID |
| `fEnterpriseInfoID` | int | 是 |  | 否 |  | 用户ID |
| `Id` | int |  | 是 | 否 |  | 自增ID |
| `SignInvoice` | varchar(200) |  |  |  |  | 专票提醒确认函地址 |
| `isSignInvoice` | tinyint |  |  |  |  | 是否已签章 0：否，1：是 |

## T_PProduct_AgreementRelation

*多险种合同与服务模板关系表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `fAgreementID` | int | 是 |  | 否 | 0 | 关联T_PProduct_Agreement表ID |
| `fServeTempID` | int | 是 |  | 否 | 0 | 关联T_PProduct_ServeTemplate表ID |
| `CreateTime` | datetime |  |  |  | getdate() | 创建时间 |

## T_ZX_GoodsRecord

*振鑫小程序-商品兑换记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fZXUserID` | int |  |  |  |  | 关联T_ZX_User表ID |
| `fGoodsID` | int |  |  |  | 0 | 商品ID，关联T_ZX_GoodsInfo商品表ID |
| `cGoodsName` | nvarchar(50) |  |  |  |  | 商品名称 |
| `cGoodsPic` | varchar(200) |  |  |  |  | 商品图片地址 |
| `cGoodsDes` | nvarchar(300) |  |  |  |  | 商品简单描述 |
| `cNewGuid` | varchar(50) |  |  |  |  | 订单编号 |
| `fState` | tinyint |  |  |  | 99 | 状态：5待发货，7待收货，10已完成 |
| `fSumPoints` | int |  |  |  |  | 实际支付总额所需积分 |
| `fPoints` | int |  |  |  | 0 | 商品单价所需积分 |
| `fGoodsCount` | int |  |  |  | 0 | 兑换数量 |
| `cRemarks` | nvarchar(100) |  |  |  |  | 下单备注信息 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |

## T_Guarantee_Claim

*保函索赔表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cNewGuid` | varchar(50) | 是 |  | 否 |  | 投保码（外键关联保单表Guarantee） |
| `claim_reason` | nvarchar(400) |  |  |  |  | 索赔原因 |
| `claimer_name` | nvarchar(100) |  |  | 否 |  | 索赔人名称 |
| `claimer_code` | nvarchar(20) |  |  | 否 |  | 索赔人代码（统一社会信用代码或组织机构代码） |
| `agent_phone` | varchar(20) |  |  |  |  | 经办人联系电话 |
| `agent_email` | varchar(40) |  |  |  |  | 经办人邮箱 |
| `amount` | decimal(18,2) |  |  | 否 |  | 索赔金额 |
| `receive_account` | varchar(50) |  |  | 否 |  | 索赔账号 |
| `receive_account_name` | nvarchar(100) |  |  | 否 |  | 索赔账号名称 |
| `receive_bank_name` | nvarchar(100) |  |  | 否 |  | 索赔账号开户行名称 |
| `receive_bank_no` | varchar(50) |  |  |  |  | 索赔账号开户行行号 |
| `claim_evidence_url` | nvarchar(1000) |  |  |  |  | 索赔证明材料下载路径 |
| `state` | tinyint |  |  |  |  | 审核结果（0：审核中，1：审核通过，2：审核不通过） |
| `error` | nvarchar(100) |  |  |  |  | 错误信息（审核不通过原因或处理失败原因） |
| `IsSent` | tinyint |  |  | 否 | 0 | 是否已发送（默认0未发送，1已发送) |
| `createTime` | datetime |  |  | 否 | getdate() |  |
| `tDelTime` | datetime |  |  |  |  |  |
| `reportNo` | varchar(50) |  |  |  |  |  |
| `reportedClaimsFile` | varchar(200) |  |  |  |  | 赔付附件 |
| `fIsPushPrc` | tinyint |  |  | 否 | 0 | 推送中心字段 根据T_Guarantee_Info表claimsState对应的状态*10+1 表示是否已推送 |
| `repaystatus` | tinyint |  |  | 否 | 0 | 是否追偿成功 0默认 1 是 2 否 |
| `repayremark` | nvarchar(100) |  |  |  |  | 备注，追偿失败需要说明理由 |
| `repaydate` | datetime |  |  |  |  | 追偿成功日期 |
| `repayamount` | decimal(10,2) |  |  |  |  | 追偿成功金额 |
| `iszbrcooperate` | tinyint |  |  | 否 | 0 | 追偿时招标人是否提供了配合 0 默认 1 是 2 否 |
| `repayIsPush` | tinyint |  |  | 否 | 0 | 追偿是否推送中心 0 否 1 是 |

## T_PProduct_QuitGuaranteeAuditLog

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  |  |  | 保单表cNewGuid |
| `fQuitState` | tinyint |  |  | 否 | 0 | 保单表fQuitState 可为0 |
| `cAuditUserName` | nvarchar(50) |  |  |  |  | 操作人 |
| `cOperationType` | nvarchar(50) |  |  |  |  | 操作步骤说明 如 (添加退保记录，退保成功) |
| `cRemark` | nvarchar(200) |  |  |  |  | 备注 |
| `tCreateTime` | datetime |  |  |  | getdate() |  |

## T_CoInsurance_Log

*共保推送日志*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `PolicyNo` | varchar(50) | 是 |  | 否 |  | 主承保单号 |
| `coinsurance_id` | int | 是 |  | 否 |  | 共保配置表id |
| `fState` | tinyint |  |  | 否 | 0 | 0：未推送，1：已推送 |
| `tdate` | datetime |  |  | 否 | getdate() | 添加时间 |
| `PushTime` | datetime |  |  |  |  | 推送时间 |
| `cPolicyNo_Cg` | varchar(50) |  |  |  |  |  |
| `cPolicyUrl_Cg` | varchar(500) |  |  |  |  |  |
| `cPolicyPzUrl_Cg` | varchar(500) |  |  |  |  |  |
| `UUID_Cg` | varchar(60) |  |  |  |  |  |
| `ErrorInfor_Cg` | varchar(500) |  |  |  |  |  |
| `fZt` | tinyint |  |  | 否 | 0 |  |
| `id` | int |  | 是 | 否 |  |  |
| `cPGPolicyUrl_Cg` | varchar(500) |  |  |  |  | 批单后的保单下载地址 |
| `cPGPolicyPzUrl_Cg` | varchar(500) |  |  |  |  | 批改后的凭证下载地址 |
| `cPGUUID_Cg` | varchar(60) |  |  |  |  | 批单UUID |
| `tPolicyTime` | datetime |  |  |  |  | 人保保单生成时间 |
| `fPiciNo` | int |  |  |  |  |  |
| `cAuditUserName` | nvarchar(10) |  |  |  |  |  |
| `tTbTime` | datetime |  |  |  |  |  |
| `fTbZt` | tinyint |  |  | 否 | 0 |  |

## T_XK_AuthRecord

*返点申请审核记录*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fType` | tinyint |  |  |  |  | 审核类型 1：返点申请审核； |
| `fRelationID` | int |  |  |  |  | RebateInfo表id； |
| `cCreateUser` | nvarchar(20) |  |  |  |  | 创建人 |
| `cCreateUserID` | nvarchar(50) |  |  |  |  | 创建人ID，关联user表ID |
| `fStatus` | tinyint |  |  |  |  | 审核结果（0：不通过；1：通过） |
| `cDesc` | nvarchar(100) |  |  |  |  | 审核意见 |
| `tCreateTime` | datetime |  |  |  |  | 创建时间 |
| `cAuthUser` | nvarchar(50) |  |  |  | (0) | 审核人 |
| `tAuthTime` | datetime |  |  |  |  | 审核时间 |

## T_PProduct_Annex

*多险种配置后台附件明细表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cTypeName` | varchar(50) |  |  |  |  | 文件类型名称 |
| `fTableID` | int |  |  |  | 0 | 业务表字段ID值 |
| `cUUid` | varchar(150) |  |  |  |  | 当fTableID不满足时，存入唯一标识 |
| `cUrl` | varchar(150) |  |  |  |  | 文件地址 |
| `CreateTime` | datetime |  |  |  | getdate() |  |
| `fUserName` | varchar(150) |  |  |  |  | 操作人姓名 |
| `cRemarks` | nvarchar(300) |  |  |  |  | 备注 |
| `cFileName` | nvarchar(100) |  |  |  |  |  |

## T_GzZrx_PackageOption

*套餐方案表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPackageID` | int |  |  | 否 | 0 | 套餐表id |
| `cOptionCode` | varchar(50) |  |  | 否 |  | 套餐方案编码 |
| `cOptionName` | nvarchar(50) |  |  | 否 |  | 套餐方案名称 |
| `cWorkCode` | varchar(20) |  |  |  |  | 职业类型代码 取自 worktype表 |
| `cWorkAlias` | nvarchar(50) |  |  |  |  | 职业别名 |
| `fPremium` | decimal(18,2) |  |  | 否 | 0 | 保费 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |

## T_GzZrx_HYX_Guarantee

*货运险订单表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  | 否 |  | 唯一性标识 |
| `fState` | tinyint |  |  |  | 0 | 订单状态（0默认草稿，1已退保，10待支付，12付款异常，14待出单，16已出单；17：已失效） |
| `cProductName` | nvarchar(50) |  |  |  |  | 保险产品 |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `cEnterpriseName` | nvarchar(50) |  |  |  |  | 企业名称 |
| `cEnterpriseNameCode` | nvarchar(32) |  |  |  |  | 统一社会信用代码 |
| `cPhone` | nvarchar(50) |  |  |  |  | 联系人手机号码 |
| `fMarginAmount` | decimal(18,2) |  |  | 否 | 0 | 保证金金额 |
| `fPrcEnsuranceId` | int |  |  | 否 | 0 | 平台id  T_GzZrx_PRCInsurance |
| `cInsuranceCompany` | nvarchar(50) |  |  |  |  | 保险公司名称 |
| `cInsuranceTypeNo` | varchar(50) |  |  |  |  | 险种编码，关联T_GzZrx_Insurance表cProNo |
| `fPackageId` | int |  |  |  |  | 套餐方案id  (T_GzZrx_Package) |
| `cPackageCode` | varchar(50) |  |  |  |  | T_GzZrx_Package编码 |
| `fInsuredChk` | tinyint |  |  |  | 1 | 被保险信息，1同投保人一致，2与投保人不一致 |
| `cOwner` | nvarchar(50) |  |  |  |  | 被保险人 |
| `cOwnerCode` | nvarchar(32) |  |  |  |  | 被保险人信用代码 |
| `cOwnerPhone` | nvarchar(50) |  |  |  |  | 被保险人手机号 |
| `cGlg` | nvarchar(50) |  |  |  |  | 公路港-货运险专属字段 |
| `fGoodsType` | tinyint |  |  |  |  | 货物种类 (1、普货；2、食品普货；3、易碎品；4、电子/机械配件；5、化工品(非危化品；6、其他)-货运险专属字段 |
| `fPackageType` | tinyint |  |  |  |  | 包装方式(1、纸箱；2、木箱；3、袋装；4、托盘；5、桶装；6、其他)-货运险专属字段 |
| `cStartProvinceCode` | varchar(8) |  |  |  |  | 起运地（省）-货运险专属字段 |
| `cStartCityCode` | varchar(8) |  |  |  |  | 起运地（市）-货运险专属字段 |
| `cStartDetailAddress` | nvarchar(150) |  |  |  |  | 起运详细地址-货运险专属字段 |
| `cEndProvinceCode` | varchar(8) |  |  |  |  | 目的地（省）-货运险专属字段 |
| `cEndCityCode` | varchar(8) |  |  |  |  | 目的地（市）-货运险专属字段 |
| `cEndDetailAddress` | nvarchar(150) |  |  |  |  | 目的地详细地址-货运险专属字段 |
| `tBeginTransTime` | datetime |  |  |  |  | 起运时间 |
| `fIsGuache` | tinyint |  |  |  | 0 | 是否挂车（0：否；1：是）-货运险专属字段 |
| `cCarNo` | nvarchar(10) |  |  |  |  | 车牌号-货运险专属字段 |
| `cGuaCarNo` | nvarchar(10) |  |  |  |  | 挂车牌号-货运险专属字段 |
| `fCarType` | tinyint |  |  |  |  | 运输工具类型（1、全封闭式卡车；2、半封闭式卡车；3、集装箱卡车；4、平板；5、高栏车；6、其他）-货运险专属字段 |
| `cGoodsPic` | nvarchar(2000) |  |  |  |  | 货物照片 |
| `cDeliverPic` | nvarchar(200) |  |  |  |  | 运单照片 |
| `cLicensePic1` | nvarchar(200) |  |  |  |  | 营业执照照片（企业）/身份证正面照片（个人） |
| `cLicensePic2` | nvarchar(200) |  |  |  |  | 授权书照片（企业）/身份证反面照片（个人） |
| `tGuaranteedTime_begin` | datetime |  |  |  |  | 保险期限 保险起期 |
| `tGuaranteedTime_end` | datetime |  |  |  |  | 保险期限  保险止期 |
| `fRate` | decimal(18,4) |  |  |  | 0 | 费率 |
| `fPremium` | decimal(18,2) |  |  |  | 0 | 保费(元) |
| `fPayType` | int |  |  |  | 0 | 支付方式  1：余额支付；2：微信支付 |
| `tPayTime` | datetime |  |  |  |  | 保费支付时间 |
| `cPolicyNo` | nvarchar(50) |  |  |  |  | 人保保单号 |
| `cPolicyUrl` | varchar(500) |  |  |  |  | 人保保单下载地址 |
| `cPolicyLocalUrl` | varchar(500) |  |  |  |  | 人保保单本地地址 |
| `tReceivePolicyTime` | datetime |  |  |  |  | 保单接收时间 |
| `tPolicyTime` | datetime |  |  |  |  | 保司保单生成时间 |
| `tGuaranteedTime` | datetime |  |  |  |  | 出函时间 |
| `CreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |
| `PRC_id` | int |  |  | 否 | 0 | T_GzZrx_PRC  表id |
| `platformcode` | nvarchar(50) |  |  |  |  | 平台编码（二级渠道编码 对应 T_GzZrx_PRC  code） |
| `fProgrammeId` | int |  |  | 否 | 0 | T_GzZrx_PRCProgramme 表id |
| `ErrorInfor` | nvarchar(200) |  |  |  |  | 异常信息 |
| `tQuitApplyTime` | datetime |  |  |  |  | 退保申请时间 |
| `fIsFPapply` | tinyint |  |  |  | 0 | 是否申请发票 （0：未申请；1：已申请） |
| `cUserId` | varchar(50) |  |  |  |  | 投保人id |
| `fInvoiceType` | tinyint |  |  |  | 0 | 发票类型：0普票电子发票，2专票纸质发票 |
| `tLastModifyTime` | datetime |  |  |  | getdate() | 订单最后操作时间 |

## T_PProduct_Regulator

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(50) |  |  |  |  | 监管单位名称 |
| `cCode` | nvarchar(50) |  |  |  |  | 监管单位编码 |
| `cProvinceName` | nvarchar(50) |  |  |  |  | 监管单位省名称 |
| `cProvinceCode` | nvarchar(50) |  |  |  |  | 监管单位省编码 |
| `cCityName` | nvarchar(50) |  |  |  |  | 监管单位城市名称 |
| `cCityCode` | nvarchar(50) |  |  |  |  | 监管单位城市编码 |
| `cAreaName` | nvarchar(50) |  |  |  |  | 监管单位区名称 |
| `cAreaCode` | nvarchar(50) |  |  |  |  | 监管单位区编码 |
| `tCreateTime` | datetime |  |  |  |  |  |

## T_PProduct_Claim

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  | 否 |  | 投保码（外键关联保单表Guarantee） |
| `claim_reason` | nvarchar(MAX) |  |  | 否 |  | 索赔原因,(理赔说明) |
| `claimer_name` | nvarchar(100) |  |  | 否 |  | 索赔人名称 |
| `claimer_code` | nvarchar(20) |  |  | 否 |  | 索赔人代码（统一社会信用代码或组织机构代码） |
| `agent_name` | nvarchar(200) |  |  |  |  | 经办人姓名（申请理赔单位联系人姓名） |
| `agent_phone` | varchar(20) |  |  |  |  | 经办人电话（申请理赔单位联系人电话） |
| `agent_email` | varchar(40) |  |  |  |  | 经办人邮箱 |
| `amount` | decimal(18,2) |  |  | 否 |  | 索赔金额 |
| `receive_account` | varchar(50) |  |  |  |  | 索赔账号 |
| `receive_account_name` | nvarchar(100) |  |  |  |  | 索赔账号名称 |
| `receive_bank_name` | nvarchar(100) |  |  |  |  | 索赔账号开户行名称 |
| `receive_bank_no` | varchar(12) |  |  |  |  | 索赔账号开户行行号 |
| `claim_evidence_url` | nvarchar(1000) |  |  |  |  | 索赔证明材料下载路径 |
| `state` | tinyint |  |  |  | 0 | 状态，默认0待确认，4理赔中，6完成理赔，9退回，10拒绝理赔 |
| `error` | nvarchar(100) |  |  |  |  | 错误信息（审核不通过原因或处理失败原因） |
| `IsSent` | tinyint |  |  | 否 | 0 | 是否已发送（默认0未发送，1已发送) 2受理已推送(安薪泰山) |
| `createTime` | datetime |  |  |  |  | 创建时间 |
| `tApplyTime` | datetime |  |  |  |  | 申请时间（后台填写） |
| `tPayTime` | datetime |  |  |  |  | 付款赔付日期（后台填写） |
| `claim_orderno` | nvarchar(200) | 是 |  | 否 |  | 申请理赔编号 |
| `claim_remark` | nvarchar(500) |  |  |  |  | 监管单位意见 |
| `claim_policyno` | nvarchar(200) |  |  |  |  | 申请保单号 |
| `actual_amount` | decimal(18,2) |  |  | 否 | 0 | 实际赔付金额 |
| `reportNo` | varchar(50) |  |  |  |  | 报案号 |
| `receiverName` | nvarchar(50) |  |  |  |  | 受理人 |
| `receiverTime` | datetime |  |  |  |  | 受理时间 |
| `tFinishTime` | datetime |  |  |  |  |  |
| `performNo` | nvarchar(300) |  |  |  |  |  |
| `hasClaimInfo` | tinyint |  |  |  |  |  |
| `claimInfoUrl` | nvarchar(200) |  |  |  |  |  |
| `organ_name` | nvarchar(100) |  |  |  |  | 金融机构理赔联系人姓名 |
| `organ_phone` | varchar(50) |  |  |  |  | 金融机构理赔经办人手机号 |
| `organ_cInsuranceName` | nvarchar(50) |  |  |  |  | 赔付机构全称 |
| `organ_cInsuranceCode` | nvarchar(50) |  |  |  |  | 赔付机构统一社会信用代码 |
| `organ_bank_name` | nvarchar(100) |  |  |  |  |  |
| `organ_bank_account` | nvarchar(50) |  |  |  |  |  |
| `organ_reason` | nvarchar(3000) |  |  |  |  |  |

## T_GzZrx_RoleMenus

*雇主责任险-角色菜单关系表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `Id` | varchar(50) | 是 |  | 否 |  |  |
| `CreateDateTime` | datetime |  |  | 否 |  |  |
| `IsDeleted` | bit |  |  | 否 |  |  |
| `MenuId` | varchar(50) |  |  | 否 |  |  |
| `RoleId` | varchar(50) |  |  | 否 |  |  |

## T_Coupon_Info

*优惠券发放使用记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `platformcode` | varchar(50) |  |  | 否 |  | 平台编码 |
| `fEnterpriseInfoID` | int |  |  |  | 0 | 企业表ID |
| `fGuaranteeID` | int |  |  |  | 0 | 表单表ID |
| `fTypeID` | int |  |  |  | 0 | 优惠券类型表ID |
| `fState` | tinyint |  |  |  | 0 | 优惠券状态，默认0未激活，1未使用，3锁定，6已使用 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |
| `tLockTime` | datetime |  |  |  |  | 锁定时间 |
| `tUseTime` | datetime |  |  |  |  | 使用时间 |
| `tStartTime` | datetime |  |  |  |  | 有效期开始时间 |
| `tEndTime` | datetime |  |  |  |  | 有效期结束时间 |
| `fZXUserID` | int |  |  |  | 0 | 关联T_ZX_User表ID |

## T_Relation_PRCEnInsuranceAttach

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `PRC_id` | int |  |  | 否 |  |  |
| `Insurance_id` | int |  |  | 否 |  |  |
| `Rate` | decimal(10,2) |  |  | 否 |  | 费率 |
| `MinfPremium` | decimal(10,2) |  |  | 否 |  | 保底收费 |
| `operator` | varchar(3) |  |  | 否 |  | 对比操作符 |
| `operatorAmount` | decimal(18,2) |  |  | 否 |  | 对比保证金金额 |
| `px` | smallint |  |  | 否 | (0) | 优先级，数值越大优先级越高 |
| `operatorType` | tinyint |  |  | 否 | 1 |  |
| `operatorProjectType` | nvarchar(50) |  |  |  |  |  |
| `ApiParameters` | nvarchar(200) |  |  |  |  |  |

## T_DaPingMu_LogOpenId

*大屏幕日志推送openId*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fLogID` | int |  |  |  | 0 | 关联T_DaPingMu_Log表ID |
| `openId` | varchar(50) |  |  |  |  |  |
| `fopenIdType` | tinyint |  |  |  | 0 | openid属于，默认0微信，1钉钉 |

## T_PProduct_BaseFile

*附件基本类型表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cNumber` | varchar(50) | 是 |  | 否 |  | 序列号编码 |
| `cName` | nvarchar(50) |  |  |  |  | 名称 |
| `fType` | tinyint |  |  |  | 0 | 类型，0新履约平台 |
| `CreateTime` | datetime |  |  |  | getdate() |  |
| `ID` | int |  | 是 | 否 |  |  |
| `fFlieType` | tinyint |  |  |  |  |  |

## T_PProduct_Serve

*多险种服务*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cServerRiskID` | nvarchar(200) |  |  | 否 |  |  |
| `cServerDetailID` | nvarchar(200) |  |  |  |  |  |
| `cFileName` | nvarchar(200) |  |  |  |  | 附件名称 |
| `cFileUrl` | varchar(200) |  |  |  |  | 附件地址 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cServeNum` | varchar(50) |  |  |  |  | T_PProduct_Serve关联字段cServeNum |
| `cFileDesc` | nvarchar(500) |  |  |  |  | 整改附件描述 |

## T_GzZrx_RolesType

*雇主责任险-用户角色类型表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `cTypeCode` | varchar(50) | 是 |  | 否 |  | 编码 |
| `cTypeName` | nvarchar(50) |  |  |  |  | 名称 |
| `fOrder` | int |  |  |  | 0 | 排序 |

## T_Pay_Log_Intranet

*支付记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `transno` | varchar(50) | 是 |  | 否 |  | 银行流水号 |
| `transtime` | datetime |  |  | 否 |  | 支付时间 |
| `transamount` | decimal(18,2) |  |  | 否 |  | 支付金额 |
| `payeracctno` | varchar(50) |  |  | 否 |  | 付款卡号 |
| `payeracctname` | nvarchar(50) |  |  | 否 |  | 付款户名 |
| `abstractinfo` | nvarchar(50) |  |  |  |  | 备注 |
| `oppositebankno` | varchar(50) |  |  | 否 |  | 付款行号 |
| `oppositebankname` | nvarchar(50) |  |  | 否 |  | 付款行名 |
| `tdate` | datetime |  |  | 否 | getdate() | 日期 |
| `OrderNo` | varchar(50) |  |  |  |  | 订单号 |
| `fState` | tinyint |  |  | 否 | 0 | 0:未使用，1：已使用，2：退款中，3：已退款 |
| `skAccount` | varchar(50) |  |  |  |  | 收款账号 |
| `dataType` | tinyint |  |  | 否 | 0 |  |
| `cardType` | tinyint |  |  | 否 | 0 |  |
| `fImportLogID` | int |  |  | 否 | 0 |  |

## T_Coupon_TaskLog

*优惠券抽奖记录*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cName` | nvarchar(30) |  |  |  |  | 任务名称 |
| `CreateTime` | datetime |  |  |  | getdate() |  |
| `platformcode` | varchar(50) |  |  |  |  | 平台编码 |
| `fState` | tinyint |  |  |  | 0 | 默认0开启，1关闭 |

## T_Relation_PRCEnInsuranceEngagedesc

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `PRC_id` | int | 是 |  | 否 |  | T_PRC_Info表id |
| `EngagedescContent` | nvarchar(2000) |  |  | 否 |  | 特约内容，带占位符 |
| `cTitle` | nvarchar(100) |  |  |  |  |  |
| `cInsuranceCompany` | nvarchar(50) | 是 |  | 否 | '人保' |  |
| `CreateTime` | datetime |  |  | 否 | getdate() |  |
| `cAuditUserName` | nvarchar(20) |  |  |  |  |  |
| `tUpdateTime` | datetime |  |  |  |  |  |
| `EngagesIsNull` | tinyint |  |  | 否 | 0 | 特约节点是生效 默认0 传1则无效即特约节点会被移除 |

## T_GzZrx_PRCInsurancePackage

*承保表与承保套餐关联表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCInsuranceID` | int |  |  | 否 | 0 | 承保表id |
| `fPackageID` | int |  |  | 否 | 0 | 套餐表id |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |

## T_PProduct_ServeCompany

*服务机构表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `platformCode` | varchar(50) |  |  |  |  | 平台编号 |
| `cCompanyName` | nvarchar(500) |  |  |  |  |  |
| `cCompanyID` | nvarchar(500) |  |  |  |  |  |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `fStatus` | tinyint |  |  |  | 0 | 状态：0禁用，1正常 |
| `cInsuranceCompany` | nvarchar(50) |  |  |  |  | 保司 |

## T_Enterprise_Black_ImportLog

*黑名单拦截导入表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fTag` | int |  |  |  | 0 | 导入类型标签默认0无，1选择网点导入 |
| `fRelatedID` | int |  |  |  | 0 | 关联ID |
| `cFileUrlName` | nvarchar(50) |  |  |  |  | 导入数据表文件名 |
| `cFileUrl` | varchar(300) |  |  |  |  | 导入数据表文件下载地址 |
| `cErr_FileUrlName` | nvarchar(50) |  |  |  |  | 导入错误数据表文件名 |
| `cErr_FileUrl` | varchar(300) |  |  |  |  | 导入错误数据表文件下载地址 |
| `fState` | tinyint |  |  |  | 0 | 导入状态：默认0未导入，1导入成功 |
| `cAuditUserName` | nvarchar(50) |  |  |  |  |  |
| `tdate` | datetime |  |  |  | getdate() |  |

## T_Pay_Log_CashierConfig

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `insuranceName` | nvarchar(50) |  |  | 否 |  | 收款机构名称 |
| `pay001` | bit |  |  | 否 | 0 | 是否支付0.01 |
| `APP_ID` | varchar(50) |  |  | 否 |  |  |
| `MY_PRIVATE_KEY` | varchar(2000) |  |  | 否 |  |  |
| `APIGW_PUBLIC_KEY` | varchar(300) |  |  | 否 |  |  |
| `Mer_id` | varchar(50) |  |  | 否 |  |  |
| `Mer_prtcl_no` | varchar(50) |  |  | 否 |  |  |
| `tdate` | datetime |  |  | 否 | getdate() |  |
| `isQrCode` | bit |  |  | 否 | 1 |  |
| `webDomain` | varchar(60) |  |  |  |  | 收银台支付页面域名 |

## T_Relation_PRCEnInsuranceFileTemplate

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCEnInsuranceID` | int |  |  | 否 | 0 |  |
| `fInsuranceFileTemplateID` | int |  |  | 否 | 0 |  |
| `fInsuranceFileTemplateBaseID` | int |  |  | 否 | 0 |  |
| `fInsuranceFileID` | int |  |  | 否 | 0 |  |
| `fIsSync` | tinyint |  |  | 否 | 1 |  |
| `tSyncTime` | datetime |  |  |  |  |  |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_PProduct_ClaimFile

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fClaimID` | int |  |  |  |  |  |
| `cFileName` | nvarchar(500) |  |  |  |  |  |
| `cFileUrl` | nvarchar(500) |  |  |  |  |  |
| `fFileType` | nvarchar(500) |  |  |  |  |  |

## T_PProduct_ServeDetail

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cServeNum` | varchar(50) |  |  |  |  | T_PProduct_Serve表cServeNum |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `cServerDetailID` | nvarchar(200) |  |  |  |  | 服务细项ID |
| `cServerDetailName` | nvarchar(200) |  |  |  |  | 服务细项名称 |
| `cServerItemID` | nvarchar(200) |  |  |  |  | 服务子项ID |
| `cServerItemName` | nvarchar(200) |  |  |  |  | 服务子项名称 |
| `cServiceDetailDesc` | nvarchar(500) |  |  |  |  | 服务细项总结 |
| `fIsPack` | tinyint |  |  |  | 0 | 是否已打包，1是，0否 |
| `cServerDetailsType` | varchar(200) |  |  |  |  | 服务细项类型 |
| `cServerDetailsRemark` | nvarchar(200) |  |  |  |  | 服务细项备注 |
| `cServerDetailFileUrl` | nvarchar(500) |  |  |  |  |  |

## T_Coupon_User

*优惠券用户统计表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `platformcode` | varchar(50) |  |  |  |  | 平台编码 |
| `fEnterpriseInfoID` | int |  |  |  | 0 | 企业表ID |
| `fTotal` | int |  |  |  | 0 | 总计 |
| `fUsed` | int |  |  |  | 0 | 已经激活过统计 |
| `fLocking` | int |  |  |  | 0 | 锁定的统计 |
| `fLeft` | int |  |  |  | 0 | 剩余可用统计 |
| `fZXUserID` | int |  |  |  | 0 |  |

## T_Relation_PRCEnInsuranceTmpContent

*电子保函动态模板*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `PRC_id` | int | 是 |  | 否 | 0 | 中心ID |
| `cInsuranceCompany` | nvarchar(50) | 是 |  | 否 |  | 保险公司 |
| `cContent` | nvarchar(3000) |  |  |  |  | 动态保函模板内容 |
| `cTitle` | nvarchar(100) |  |  |  |  | 标题 |
| `CreateTime` | datetime |  |  |  |  |  |
| `cAuditUserName` | nvarchar(20) |  |  |  |  | 操作人 |
| `tUpdateTime` | datetime |  |  |  |  | 最新修改时间 |

## T_PProduct_ClaimInfo

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `claim_orderno` | nvarchar(200) | 是 |  | 否 |  | 申请理赔编号 |
| `nmg_user` | nvarchar(50) |  |  |  |  | 农民工姓名 |
| `nmg_idcard` | nvarchar(50) | 是 |  | 否 |  | 农民工身份证号码 |
| `nmg_idcard_enddate` | datetime |  |  |  |  | 农民工身份证截止日期 |
| `nmg_sex` | nvarchar(50) |  |  |  |  | 农民工性别;安薪泰山工资卡开户银行名称 |
| `nmg_address` | nvarchar(255) |  |  |  |  | 农民工住址 安薪泰山序号 |
| `nmg_phone` | nvarchar(50) |  |  |  |  | 农民工手机号码 |
| `nmg_bankname` | nvarchar(50) |  |  |  |  | 农民工银行卡开户行 |
| `nmg_bankcardno` | nvarchar(50) |  |  |  |  | 农民工银行卡账号 |
| `nmg_planamount` | decimal(18,2) |  |  |  |  | 应付金额 |
| `status` | int |  |  |  |  | 是否支付成功，如成功为0，如不成功为1 |
| `claimamount` | decimal(18,2) |  |  |  |  | 农民工获赔金额 |
| `errormsg` | varchar(255) |  |  |  |  | 不成功原因 |

## T_PRC_Interface

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `platformcode` | varchar(50) |  |  | 否 |  | 平台编码 |
| `cInsuranceCompany` | nvarchar(50) |  |  |  |  | 机构简称 |
| `message` | nvarchar(200) |  |  |  |  | 返回信息 |
| `fState` | tinyint |  |  | 否 | 0 | 0 未生效 1 生效 |
| `tdate` | datetime |  |  | 否 | getdate() | 创建时间 |

## T_PProduct_ServeDetailAttachment

*服务细项附件列表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cServerDetailID` | nvarchar(200) |  |  |  |  | 服务细项编号(以三和系统为准) |
| `cServerDetailFileUrl` | nvarchar(200) |  |  |  |  | 附件地址 |
| `cServerDetailFileName` | nvarchar(200) |  |  |  |  | 附件名称 |
| `cServerDetailFileDesc` | nvarchar(200) |  |  |  |  | 附件描述 |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `cServeNum` | varchar(50) |  |  |  |  | T_PProduct_Serve关联字段cServeNum |

## T_Enterprise_BlackPRC

*黑名单拦截设置表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `fBlackID` | int | 是 |  | 否 |  | 关联T_Enterprise_Black表ID |
| `fPRCEnInsuranceID` | int | 是 |  | 否 | 0 | 关联T_Relation_PRCEnInsurance表ID |
| `fDisableType` | tinyint |  |  |  | 0 | 禁用类型，默认0永久，1短期 |
| `tEndTime` | datetime |  |  |  |  | 禁用止期 |
| `fZt` | tinyint |  |  |  | 0 | 有效性，默认0有效，1无效 |
| `UpdateTime` | datetime |  |  |  | getdate() |  |

## T_CX_Order

*订单表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cTransCode` | varchar(50) |  |  | 否 |  | 业务流水号 |
| `fProductId` | int |  |  | 否 |  | 产品id |
| `cOrderNo` | nvarchar(50) |  |  | 否 |  | 保单号 |
| `tCreateDate` | datetime |  |  | 否 | getdate() | 添加时间 |
| `cAutobikeRackNo` | nvarchar(50) |  |  | 否 |  | 车架号 |
| `tRegisterDate` | datetime |  |  | 否 |  | 初登日期/购车日期 |
| `cPurchaseAreaCode` | varchar(10) |  |  | 否 |  | 购车区域行政区划编码 |
| `cPurchaseAreaName` | nvarchar(50) |  |  |  |  |  |
| `cOwnerName` | nvarchar(20) |  |  | 否 |  | 车主姓名 |
| `cOwnerCardID` | varchar(20) |  |  | 否 |  | 车主身份证号 |
| `cOwnerMobile` | varchar(20) |  |  | 否 |  | 车主手机号 |
| `cReason` | nvarchar(200) |  |  |  |  | 退保原因 |
| `tStartTime` | datetime |  |  | 否 |  | 起保日期 |
| `tEndTime` | datetime |  |  | 否 |  | 终保日期 |
| `fStatus` | tinyint |  |  |  | 1 | 状态（1：在保；2：退保） |
| `tQuitStartTime` | datetime |  |  |  |  | 退保生效时间 |
| `fQuitState` | tinyint |  |  |  | 0 | 退保状态 0未处理 1已退保 2已驳回 3处理中 |
| `fIsPush` | tinyint |  |  |  | 0 | 是否已经推送，默认0未推送，1推送成功, |
| `tPushTime` | datetime |  |  |  |  | 推送时间 |
| `tPushSuccessTime` | datetime |  |  |  |  | 成功推送记录时间 |
| `fQuitIsPush` | tinyint |  |  | 否 | 0 | 退保推送 |
| `cPushFailReason` | nvarchar(500) |  |  |  |  | 参保推送失败原因 |
| `tQutiPushSuccessTime` | datetime |  |  |  |  | 退保成功推送记录时间 |
| `cQuitPushFailReason` | nvarchar(500) |  |  |  |  | 退保推送失败原因 |
| `cPolicyNo` | nvarchar(50) |  |  | 否 |  | 每月团单号 |
| `cChannelNo` | nvarchar(50) |  |  |  |  | 渠道编码 |
| `cQuitChannelNo` | nvarchar(50) |  |  |  |  |  |

## T_GzZrx_Programme

*方案表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fInsuranceInfoID` | int |  |  | 否 | 0 | 金融机构表id |
| `fInsuranceTypeID` | int |  |  | 否 | 0 | 险种表id |
| `cProgrammeCode` | varchar(50) |  |  | 否 |  | 方案编码 |
| `cProgrammeName` | nvarchar(50) |  |  | 否 |  | 方案名称 |
| `tStartTime` | datetime |  |  |  |  | 有效开始时间 |
| `tEndTime` | datetime |  |  |  |  | 有效截止时间 |
| `cRemark` | nvarchar(100) |  |  |  |  | 备注 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_PProduct_ClientMode

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cModeName` | nvarchar(50) |  |  |  |  | 模式名称 |
| `cModeCode` | nvarchar(50) |  |  |  |  | 模式编码 |
| `cModeDescribe` | nvarchar(500) |  |  |  |  | 模式描述 |
| `fClientType` | tinyint |  |  |  |  | 客户端类型 1有客户端 2无客户端（纯接口） |
| `fLoginType` | tinyint |  |  |  |  | 登陆注册类型 1渠道授权 2注册认证 3 XXX-CA |
| `fSignatureType` | tinyint |  |  |  |  | 签章类型 1线下签章  2CA签章 |
| `fAuthType` | tinyint |  |  |  |  | 认证模式 1免认证 2我司打款认证 3企业打款认证 |
| `fCustomerService` | tinyint |  |  |  |  | 客服类型  1链接型客服 2展示型客服 3无菜单客服模式 |
| `fAccountType` | tinyint |  |  |  |  | 账户类型 1企业信息+手机号 2企业信息+手机号+员工管理 3手机号 |
| `fProductAbout` | tinyint |  |  |  |  | 是否显示产品介绍 0不显示 1显示 |
| `fApplyList` | tinyint |  |  |  |  | 是否显示项目列表  0不显示 1显示 |
| `fPayLog` | tinyint |  |  |  |  | 是否显示支付列表  0不显示 1显示 |
| `fAccountEnt` | tinyint |  |  |  |  | 是否显示账户模块企业信息  0不显示 1显示 |
| `fAccountUser` | tinyint |  |  |  |  | 是否显示账户模块账户信息  0不显示 1显示 |
| `fAccountStaff` | tinyint |  |  |  |  | 是否显示账户模块子账户信息  0不显示 1显示 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cLastEditUser` | nvarchar(50) |  |  |  |  | 最后修改人 |
| `tLastEditTime` | datetime |  |  |  |  | 最后修改时间 |
| `fLoginBtn` | tinyint |  |  |  |  | 是否显示退出按钮，1显示，0不显示 |
| `IsCloseOrderBtn` | tinyint |  |  | 否 | 1 | 是否支持关闭订单，1正在办理菜单内关闭，2详情页关闭，3不可关闭 |
| `fGuaranteeInvalid` | tinyint |  |  | 否 | 0 | 是否失效订单，默认0否，1是 |
| `fIsRegister` | tinyint |  |  | 否 | 0 | 是否支持注册，默认0否，1是 |

## T_PRC_Info

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `Prc_Code` | varchar(50) |  |  | 否 |  | 公共资源中心编码 |
| `Prc_Name` | nvarchar(50) |  |  | 否 |  | 公共资源中心名字 |
| `Web_Domain` | varchar(60) |  |  | 否 |  | 网站域名 |
| `Web_Title` | nvarchar(50) |  |  | 否 |  | 网站标题 |
| `Web_Logo` | varchar(100) |  |  | 否 |  | 网站logo |
| `tdate` | datetime |  |  | 否 | getdate() | 添加时间 |
| `cCity` | nvarchar(30) |  |  |  |  |  |
| `fSupportMode` | tinyint |  |  | 否 |  | 出单模式，0线上出单，1线下出单，2独立出单，3地推模式，4担保小程序出单 |
| `fState` | tinyint |  |  | 否 | 1 | 状态：0待上线，1启用，2下线 |
| `Prc_Type` | tinyint |  |  | 否 | 0 |  |
| `cSheng` | nvarchar(30) |  |  |  |  |  |
| `cShi` | nvarchar(30) |  |  |  |  |  |
| `cQu` | nvarchar(30) |  |  |  |  |  |
| `cInsuranceCodeName` | nvarchar(20) |  |  |  |  |  |
| `Prc_FullName` | nvarchar(50) |  |  |  |  |  |
| `Prc_WebSite` | varchar(200) |  |  |  |  |  |
| `Web_Icon` | varchar(100) |  |  |  |  |  |
| `Login_Logo` | varchar(100) |  |  |  |  |  |
| `cFile_Help` | varchar(100) |  |  |  |  |  |
| `cFile_Drive` | varchar(100) |  |  |  |  |  |
| `fIsEncryption` | tinyint |  |  | 否 | 1 |  |
| `cType_Mode` | varchar(30) |  |  |  |  |  |
| `cPre_TestUrl` | varchar(100) |  |  |  |  |  |
| `cPre_FormalUrl` | varchar(100) |  |  |  |  |  |
| `cXy` | varchar(20) |  |  |  |  |  |
| `cServiceId` | varchar(100) |  |  |  |  |  |
| `cServiceUrl` | varchar(100) |  |  |  |  |  |
| `cTechSupport` | nvarchar(100) |  |  |  |  |  |
| `fPolicyType` | tinyint |  |  | 否 | 2 |  |
| `fAccountInfo` | tinyint |  |  | 否 | 1 |  |
| `fAuditType` | tinyint |  |  | 否 | 1 |  |
| `epontPushType` | varchar(10) |  |  |  |  |  |
| `fVerifyTime` | tinyint |  |  | 否 | 0 |  |
| `cSourceCodeName` | nvarchar(20) |  |  |  |  |  |
| `fSourceCodeShow` | tinyint |  |  | 否 | 0 |  |
| `cInsuranceName` | nvarchar(10) |  |  |  |  |  |
| `cServiceTel` | varchar(20) |  |  |  |  |  |
| `cServiceQQ` | varchar(20) |  |  |  |  |  |
| `cProjectShow` | varchar(10) |  |  |  |  |  |
| `tdpName` | nvarchar(20) |  |  |  |  |  |
| `fTbrEncryption` | tinyint |  |  | 否 | 0 |  |
| `cSelectDes` | varchar(30) |  |  |  |  |  |
| `cNetsRemarks` | nvarchar(200) |  |  |  |  |  |
| `fClientMode` | tinyint |  |  | 否 | 0 |  |
| `cClientModeDesc` | nvarchar(200) |  |  |  |  |  |
| `cLoginTitle1` | nvarchar(50) |  |  |  |  |  |
| `cLoginTitle2` | nvarchar(50) |  |  |  |  |  |
| `cLoginTitle3` | nvarchar(50) |  |  |  |  |  |
| `cLoginTitle4` | nvarchar(50) |  |  |  |  |  |
| `fServiceWay` | tinyint |  |  | 否 | 0 |  |
| `fWechatType` | tinyint |  |  | 否 | 0 |  |
| `cOrg` | varchar(20) |  |  |  |  |  |
| `cBrowser` | nvarchar(50) |  |  |  |  |  |
| `cNetwork` | varchar(20) |  |  |  |  |  |
| `cDeployment` | varchar(20) |  |  |  |  |  |
| `cCooperation` | varchar(20) |  |  |  |  |  |
| `cInterfaceType` | varchar(20) |  |  |  |  |  |
| `cInterfaceDoc` | varchar(200) |  |  |  |  |  |
| `cClient` | varchar(200) |  |  |  |  |  |
| `cRemarks` | nvarchar(200) |  |  |  |  | 备注说明（记录中心平台的其他特殊信息） |
| `cOfflineNotice` | nvarchar(200) |  |  |  |  | 下线通知 |

## T_ZX_GuaranteeLog

*担保保函订单操作日志表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cNewGuid` | varchar(50) |  |  |  |  | 订单号 |
| `cAuditUserName` | nvarchar(50) |  |  |  |  | 操作人 |
| `cOperationType` | nvarchar(50) |  |  |  |  | 操作类型 |
| `cRemark` | nvarchar(200) |  |  |  |  | 操作内容 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 操作时间 |

## T_PProduct_ServeDetailInfo

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cServerDetailID` | nvarchar(200) |  |  |  |  | 服务细项ID |
| `cServerDetailName` | nvarchar(200) |  |  |  |  | 服务细项名称 |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `cServerItemID` | nvarchar(200) |  |  |  |  | 服务子项ID |
| `cServerItemName` | nvarchar(200) |  |  |  |  | 服务子项名称 |
| `fIsDelete` | tinyint |  |  |  | 0 | 是否删除（0：否；1：是）（是否撤回） |
| `cServerDetailsType` | varchar(200) |  |  |  |  | 服务细项类型 |
| `cServerDetailsRemark` | nvarchar(200) |  |  |  |  | 服务细项备注 |

## T_CX_Order_Group

*团单配置表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fProductId` | int |  |  | 否 |  | 产品id |
| `cDate` | varchar(20) |  |  | 否 |  | 归属月份 |
| `cOrderNo` | nvarchar(50) |  |  | 否 |  | 保单号 |
| `tCreateDate` | datetime |  |  | 否 | getdate() | 添加时间 |
| `cChannelNo` | nvarchar(50) |  |  | 否 | N'TLLAPP' |  |
| `fChannelId` | int |  |  | 否 | 1 |  |

## T_SendMessage_Template

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cContent` | text |  |  |  |  | 模板内容 |
| `cName` | nvarchar(50) |  |  |  |  | 模板名称 |
| `fType` | int |  |  |  | 0 |  |

## T_PProduct_ServeExpert

*服务专家信息*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cInsuranceCompany` | nvarchar(30) |  |  |  |  | 保险公司，比如人保 |
| `platformCode` | varchar(50) |  |  |  |  | 平台编号 |
| `cNum` | nvarchar(200) |  |  |  |  | 专家编号 |
| `cName` | nvarchar(200) |  |  |  |  | 专家姓名 |
| `cProfession` | nvarchar(200) |  |  |  |  | 专家职业 |
| `cAddress` | nvarchar(200) |  |  |  |  | 专家居住地 |
| `cHighestEducation` | nvarchar(200) |  |  |  |  | 最高学历 |
| `fCertificateNum` | int |  |  |  |  | 证书数量 |
| `fState` | int |  |  |  |  | 状态 0停用 1启用 |
| `cPhone` | nvarchar(200) |  |  |  |  | 专家电话 |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `cNewGuid` | varchar(50) |  |  |  |  | 自定义唯一性 |

## T_PProduct_PRCEnInsuranceEnclosureGuarantee

*附件存储表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  | 企业表id |
| `cEnclosureName` | nvarchar(200) |  |  |  |  | 附件名称 |
| `cEnclosureCode` | nvarchar(150) |  |  |  |  | 附件编码 |
| `fPRCEnInsuranceEnclosureId` | int |  |  |  |  | 表id |
| `tCreateTime` | datetime |  |  |  |  | 创建时间 |
| `cLastEditUser` | nvarchar(50) |  |  |  |  | 最后修改人 |
| `tLastEditTime` | datetime |  |  |  |  | 最后修改时间 |
| `cUrl` | varchar(500) |  |  |  |  | 附件地址 |
| `cLocalUrl` | varchar(500) |  |  |  |  | ossUrl |
| `cName` | nvarchar(100) |  |  |  |  | 附件文件名称 |
| `cNewGuid` | varchar(50) |  |  |  |  | 订单号 |
| `fImageIsPush` | tinyint |  |  | 否 | 0 |  |

## T_ZX_ChannelRate

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fInsuranceFileID` | int |  |  | 否 | 0 | 担保保函模板ID |
| `cChannelCode` | varchar(50) |  |  |  |  | 一级渠道编码 |
| `cLeveltwoCode` | varchar(50) |  |  |  |  | 二级渠道编码 |
| `cChannelName` | nvarchar(50) |  |  |  |  | 渠道名称 |
| `cAttributionUser` | nvarchar(10) |  |  |  |  | 业务归属 |
| `fRate` | decimal(10,3) |  |  |  |  | 费率 |
| `fMinPremium` | decimal(10,2) |  |  |  |  | 最低保费 |
| `fState` | tinyint |  |  | 否 | 1 | 状态 0 禁用 1 启用 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_CX_PartnerChannel

*合作厂商-渠道*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cPartnerName` | nvarchar(50) |  |  | 否 |  | 合作厂商名称 |
| `cPartnetNo` | nvarchar(50) |  |  | 否 |  | 合作厂商编号 |
| `cChannelNo` | nvarchar(50) |  |  | 否 |  | 渠道编码 |
| `cChannelName` | nvarchar(50) |  |  | 否 |  | 渠道名称 |
| `cAppKey` | nvarchar(50) |  |  | 否 |  |  |
| `cAppSecret` | nvarchar(50) |  |  | 否 |  |  |

## T_XK_Contacts_UpdateLog

*联系人更新记录表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fContactsId` | int |  |  | 否 | 0 | 联系人表id |
| `cOldContent` | nvarchar(1000) |  |  |  |  | 旧内容 |
| `cContent` | nvarchar(1000) |  |  |  |  | 新内容 |
| `tUpdateUser` | nvarchar(20) |  |  |  |  | 更新人 |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_SendMode_Info

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cSendModeName` | nvarchar(200) |  |  |  |  |  |
| `cSendModeUrl` | nvarchar(200) |  |  |  |  |  |

## T_PProduct_ConstructionType

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cConstructionType` | nvarchar(50) |  |  |  |  | 资质类型 |

## T_PProduct_ServeExpertRalation

*服务与专家关系表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `cServeNum` | varchar(50) | 是 |  | 否 |  | T_PProduct_Serve关联字段cServeNum |
| `cServerItemID` | nvarchar(200) | 是 |  | 否 |  | 服务子项ID |
| `cServeExpertNum` | nvarchar(200) | 是 |  | 否 |  | 专家编号 |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |

## T_GzZrx_Package

*保额套餐表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPackageID` | int |  |  | 否 | 0 | 套餐表id |
| `cOptionCode` | varchar(50) |  |  | 否 |  | 套餐方案编码 |
| `cOptionName` | nvarchar(50) |  |  | 否 |  | 套餐方案名称 |
| `cWorkCode` | varchar(20) |  |  |  |  | 职业类型代码 取自 worktype表 |
| `cWorkAlias` | nvarchar(50) |  |  |  |  | 职业别名 |
| `fPremium` | decimal(18,2) |  |  | 否 | 0 | 保费 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |

## T_CX_Product

*车险-产品表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cProductName` | nvarchar(50) |  |  | 否 |  | 产品名称 |
| `cInsuranceCom` | nvarchar(20) |  |  | 否 |  | 保司 |
| `cPartner` | nvarchar(50) |  |  | 否 |  | 合作厂商 |
| `cProductNo` | nvarchar(20) |  |  | 否 |  | 保险编码 |
| `tCreateDate` | datetime |  |  |  | getdate() |  |
| `cInsuranceCode` | nvarchar(50) |  |  | 否 |  | 保司编码 |

## T_Settle_Info

*中心理赔资料表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fEnterpriseInfoID` | int |  |  |  |  |  |
| `cBz` | nvarchar(MAX) |  |  |  |  | 备注 |
| `cUrl` | varchar(500) |  |  |  |  | 资料上传地址 |
| `CreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `fIsPush` | bit |  |  |  | 0 | 是否已推送，默认0否，1是 |
| `tPushTime` | datetime |  |  |  |  | 推送时间 |
| `fState` | tinyint |  |  |  | 0 |  |
| `fIsDelete` | bit |  |  |  | 0 |  |
| `fGuaranteeInfoID` | int |  |  | 否 | 0 |  |

## T_GzZrx_PRCProgramme

*二级渠道与方案关联表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCID` | int |  |  | 否 | 0 | 二级渠道表id |
| `fProgrammeID` | int |  |  | 否 | 0 | 方案表id |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_PProduct_Department

*机构部门网点*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fParentID` | tinyint |  |  |  | 0 | 父级 |
| `fBusinessType` | tinyint |  |  |  | 1 | 业务类型，0现金缴纳，1保险保函，2银行保函，3担保保函 |
| `cName` | nvarchar(50) |  |  |  |  | 金融机构名称/部门名称/网点名称 |
| `cOrganization` | nvarchar(50) |  |  |  |  | 组织机构全称 |
| `cPerson` | nvarchar(30) |  |  |  |  | 负责人 |
| `cSheng` | nvarchar(30) |  |  |  |  | 省 |
| `cShi` | nvarchar(30) |  |  |  |  | 市 |
| `cQu` | nvarchar(30) |  |  |  |  | 区 |
| `cFiles` | varchar(350) |  |  |  |  | 附件 |
| `cDesc` | nvarchar(150) |  |  |  |  | 备注信息 |
| `CreateTime` | datetime |  |  |  |  | 创建时间 |
| `platformCode` | varchar(50) |  |  |  |  | 平台代码 |
| `fType` | tinyint |  |  |  | 0 | 类型，0人设部门，1金融机构，2网点 |
| `cUserID` | varchar(50) |  |  |  |  | 录入的用户ID，对应T_PProduct_Admin表ID |
| `fState` | tinyint |  |  |  | 0 | 账号状态，0正常，1禁用，2删除 |

## T_PProduct_ServeItem

*服务子项明细*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cServeNum` | varchar(50) |  |  |  |  | T_PProduct_Serve关联字段cServeNum |
| `cServerID` | nvarchar(200) |  |  |  |  | 服务ID |
| `cServerName` | nvarchar(200) |  |  |  |  | 服务名称 |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `cServePersonnelIDs` | varchar(500) |  |  |  |  | 服务专家id集合 |
| `cServiceItemDesc` | nvarchar(500) |  |  |  |  | 服务项总结 |
| `cServerItemID` | nvarchar(200) |  |  |  |  | 服务子项ID |
| `cServerItemName` | nvarchar(200) |  |  |  |  | 服务子项名称 |
| `cServePersonnelNames` | varchar(1000) |  |  |  |  | 服务专家名称集合 |
| `cServePersonnelPhone` | varchar(1000) |  |  |  |  |  |

## T_XK_Contacts_DataStatistics

*线客联系人出单数据监测统计表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cType` | varchar(50) |  |  |  |  | 规则名称 |
| `cRule` | varchar(500) |  |  |  |  | 预警规则JSON形式存放 |

## T_StateMent_Files

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fSid` | int |  |  |  |  | 对应T_StateMent_List表ID |
| `cFileUrl` | varchar(200) |  |  |  |  | 文件地址 |
| `cFileName` | nvarchar(50) |  |  |  |  | 文件名称 |
| `fFileState` | tinyint |  |  |  |  | 对账文件类型状态：0待对账，1对账失败，2对账成功 |
| `CreateTime` | datetime |  |  |  |  |  |
| `tFileStateTime` | datetime |  |  |  | (0) | 对账时间 |

## T_PProduct_DiversifiedFile

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCEnInsuranceID` | int |  |  |  |  | 对应T_PProduct_PRCEnInsurance表ID |
| `cName` | nvarchar(50) |  |  |  |  | 附件名称 |
| `cFileNumber` | varchar(50) |  |  |  |  | 对应T_Base_File表cNumber |
| `cFileUrl` | varchar(200) |  |  |  |  | 文件地址 |
| `fFileSaveType` | tinyint |  |  |  | 0 | 文件保存类型，0本地，1OSS |
| `CreateTime` | datetime |  |  |  |  |  |
| `fOrder` | int |  |  |  | 0 |  |
| `cPosX` | varchar(30) |  |  |  |  | 坐标X |
| `cPosY` | varchar(30) |  |  |  |  | 坐标Y |
| `cRemarks` | nvarchar(MAX) |  |  |  |  |  |
| `cProductTypeNo` | varchar(30) |  |  |  |  | 对应T_Insurance_Product表cProductTypeNo |
| `cProductNo` | varchar(30) |  |  |  |  | 对应T_Insurance_Product表cProductNo |
| `fPosPage` | tinyint |  |  |  | 1 | 签章页 |
| `fInsuranceTypeID` | int |  |  |  |  | 险种ID |
| `fUsePage` | int |  |  |  |  | 用途（使用页面）1：投保须知 |
| `fProgrammeID` | int |  |  |  |  | T_PProduct_Programme 表ID 方案关联ID |
| `fSuperviseID` | int |  |  | 否 | 0 |  |

## T_PProduct_ServeItemInfo

*服务明细信息（三和系统传入）*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `cServerItemID` | nvarchar(200) |  |  |  |  | 服务子项ID |
| `cServerItemName` | nvarchar(200) |  |  |  |  | 服务子项名称 |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |
| `fIsDelete` | tinyint |  |  |  | 0 | 是否删除（0：否；1：是）（是否撤回） |

## T_DaPingMu_User

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `prc_type` | int |  |  |  | 0 | 大屏幕自定义的库值 |
| `fPRCEnInsuranceID` | int |  |  |  | 0 | 对应T_Relation_PRCEnInsurance表ID |
| `prc_Code` | varchar(30) |  |  |  |  | 平台码 |
| `cInsuranceCompany` | nvarchar(20) |  |  |  |  | 机构简称 |
| `openIds` | varchar(300) |  |  |  |  | 微信openid |
| `openUsers` | nvarchar(100) |  |  |  |  | 微信openid所属用户 |
| `insurance_type` | tinyint |  |  | 否 | 0 | 默认0是投标订单业务，1多险种订单业务，2投标发票业务，3雇主责任险，4无人机险 |
| `fOpenIdType` | tinyint |  |  | 否 | 0 | openid所属于类型，默认0微信，1钉钉 |

## T_StateMent_List

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fFileType` | tinyint |  |  |  |  | 类型：0保单对账文件，1手续费对账文件 |
| `cInsuranceCompany` | nvarchar(30) |  |  |  |  | 保险公司 |
| `cPower` | nvarchar(30) |  |  |  |  | 地区中心 |
| `fDateType` | tinyint |  |  |  | 0 | 日期类型：0签单日期，1生效日期 |
| `tDateBegin` | datetime |  |  |  |  | 对账开始日期 |
| `tDateEnd` | datetime |  |  |  |  | 对账结束日期 |
| `CreateTime` | datetime |  |  |  |  |  |
| `fFileState` | int |  |  |  | -1 | -1初账，0待对账，1对账失败，2对账成功 |
| `tFileStateTime` | datetime |  |  |  |  | 最近对账时间 |

## T_PaymentSystem_Order

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `applyno` | varchar(50) | 是 |  | 否 |  | 业务流水号 |
| `biddername` | nvarchar(50) |  |  | 否 |  | 公司名称 |
| `bank` | nvarchar(50) |  |  | 否 |  | 基本户开户行 |
| `account` | varchar(50) |  |  | 否 |  | 基本户帐号 |
| `cost` | decimal(10,2) |  |  | 否 |  | 付款金额 |
| `tdate` | datetime |  |  | 否 | getdate() | 提交时间 |
| `fState` | tinyint |  |  | 否 | 0 | 0：未匹配，1：已退保，3：上传打款凭证，4：匹配成功，5：匹配异常，14：订单取消；15：超过15天未支付 |
| `payId` | int |  |  |  |  | 付款表ID |
| `insureResult` | tinyint |  |  |  |  | 0：成功，1：失败 |
| `instname` | nvarchar(50) |  |  |  |  | 承保机构名称 |
| `instcode` | varchar(50) |  |  |  |  | 承保机构编码 |
| `baohanno` | varchar(50) |  |  |  |  | 保单号 |
| `ResultTime` | datetime |  |  |  |  | 结果接收时间 |
| `cPaymentSerialNumber` | varchar(4) |  |  | 否 |  | 打款序列号 |
| `cPaymentVoucher` | varchar(100) |  |  |  |  | 打款凭证 |
| `tPaymentVoucherTime` | datetime |  |  |  |  | 打款凭证时间 |
| `platformcode` | varchar(50) |  |  |  |  | 平台编号 |
| `skAccount` | varchar(50) |  |  |  |  | 收款账号 |
| `fMarginAmount` | decimal(10,2) |  |  |  |  |  |
| `cAuditMessage` | nvarchar(50) |  |  |  |  |  |
| `cAuditUserName` | nvarchar(20) |  |  |  |  |  |
| `cRealName` | nvarchar(50) |  |  |  |  |  |
| `cPhone` | varchar(50) |  |  |  |  |  |
| `errmsg` | nvarchar(100) |  |  |  |  |  |
| `cProjectNo` | nvarchar(150) |  |  |  |  |  |
| `cChannelDesc` | nvarchar(50) |  |  |  |  |  |
| `tCancelTime` | datetime |  |  |  |  |  |
| `fXkOrderID` | int |  |  |  | 0 |  |
| `fbhIsPush` | tinyint |  |  | 否 | 0 | 经纪机构数据交互推送状态 0 未推送 1 密文已推送 2 明文已推送 |
| `ftbIsPush` | tinyint |  |  | 否 | 0 | 经纪机构数据交互推送状态 0 退保未推送 1 退保已推送 |
| `fbhTechIsPush` | tinyint |  |  | 否 | 0 | 技术机构数据交互推送状态 0 未推送 1 密文已推送 2 明文已推送 |
| `ftbTechIsPush` | tinyint |  |  | 否 | 0 | 技术机构数据交互推送状态 0 退保未推送 1 退保已推送 |

## T_PProduct_DiversifiedFileTemplate

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fBaseID` | int |  |  |  |  |  |
| `cName` | nvarchar(50) |  |  |  |  | 附件名称 |
| `cFileNumber` | varchar(50) |  |  |  |  | 对应T_Base_File表cNumber |
| `cFileUrl` | varchar(200) |  |  |  |  | 文件地址 |
| `fFileSaveType` | tinyint |  |  |  | 0 | 文件保存类型，0本地，1OSS |
| `CreateTime` | datetime |  |  |  | getdate() |  |
| `fOrder` | int |  |  |  | 0 |  |
| `cPosX` | varchar(30) |  |  |  |  | 坐标X |
| `cPosY` | varchar(30) |  |  |  |  | 坐标Y |
| `cRemarks` | nvarchar(MAX) |  |  |  |  |  |
| `cProductTypeNo` | varchar(30) |  |  |  |  | 对应T_Insurance_Product表cProductTypeNo |
| `cProductNo` | varchar(30) |  |  |  |  | 对应T_Insurance_Product表cProductNo |
| `fPosPage` | tinyint |  |  |  | 1 | 签章页 |
| `fInsuranceTypeID` | int |  |  |  |  | 险种ID |

## T_Email_Log

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `emailTitle` | nvarchar(50) |  |  | 否 |  | 标题 |
| `receiveAddress` | varchar(300) |  |  |  |  | 收件地址 |
| `xlsUrl` | varchar(200) |  |  |  |  | xls附件地址 |
| `zipUrl` | varchar(200) |  |  |  |  | zip附件地址 |
| `fstate` | tinyint |  |  | 否 | 0 | 0：未处理，1：已处理 |
| `tdate` | datetime |  |  | 否 | getdate() | 添加时间 |
| `subdate` | datetime |  |  |  |  | 处理时间 |
| `cAuditUserName` | nvarchar(50) |  |  |  |  | 处理人姓名 |
| `platformcode` | varchar(50) |  |  |  |  |  |
| `cInsuranceCompany` | nvarchar(50) |  |  |  |  |  |
| `sendCode` | varchar(50) |  |  |  |  |  |
| `fType` | tinyint |  |  | 否 | 0 |  |

## T_ZX_InsuranceShowItem

*（已废弃）保函格式指定显示字段*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fInsuranceFileTemplateId` | int |  |  |  |  |  |
| `fType` | tinyint |  |  |  |  | 类型（1：项目名称；2：项目编号；3：标段名称；4：标段编号） |
| `tCreateDate` | datetime |  |  |  | getdate() |  |

## T_GzZrx_PRCInsuranceProgramme

*承保表与方案表关联表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fPRCInsuranceID` | int |  |  | 否 | 0 | 承保表id |
| `fProgrammeID` | int |  |  | 否 |  | 方案表id |
| `tCreateTime` | datetime |  |  | 否 | getdate() |  |

## T_PProduct_ServeProject

*服务项目关联表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int |  | 是 | 否 |  |  |
| `fProjectID` | int | 是 |  | 否 |  |  |
| `fServeID` | int | 是 |  | 否 |  |  |
| `fIsDelete` | tinyint |  |  |  | 0 |  |
| `fServiceStatus` | varchar(10) |  |  |  |  | 01 正常   02 服务异常 |

## T_MobileMsg_DictType

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `cTypeCode` | varchar(20) | 是 |  | 否 |  | 字典类型编码 |
| `cTypeName` | nvarchar(20) |  |  | 否 |  | 字典类型名称 |
| `tCreateTime` | datetime |  |  | 否 | getdate() | 创建时间 |

## T_Email_sendCode

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `platformcode` | varchar(50) | 是 |  | 否 |  | 平台编码 |
| `cInsuranceCompany` | nvarchar(50) | 是 |  | 否 |  | 承保机构 |
| `sendCode` | int |  |  | 否 | 1 | 发件编号 |
| `lastdate` | datetime |  |  | 否 | getdate() |  |

## T_PRC_TypeModeSearchInfo

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fLoginType` | tinyint |  |  |  |  | 登录方式，1授权登录（类北京），2注册登录（类常德），3CA登录（福建），4CA登录（温州翔晟） |
| `fLoginTypeCheck` | tinyint |  |  |  |  | 登录方式，1授权登录（类北京），2注册登录（类常德），3CA登录（福建），4CA登录（温州翔晟） |
| `fCAType` | tinyint |  |  | 否 | 0 |  |
| `fProjectType` | tinyint |  |  |  |  | 项目信息，1全部输入-明文，2部分输入-明文，3全部推送-加密，4编码推送-加密，5无推送-加密 |
| `fProjectTypeCheck` | tinyint |  |  | 否 | 0 | 项目信息，1全部输入-明文，2部分输入-明文，3全部推送-加密，4编码推送-加密，5无推送-加密 |
| `fApplyList` | tinyint |  |  |  |  | 申请列表，1有（加密），2有（明文），3无 |
| `fApplyListCheck` | tinyint |  |  | 否 | 0 | 申请列表，1有（加密），2有（明文），3无 |
| `fFileRead` | tinyint |  |  | 否 | 0 | 文件条款读取：默认0无，1勾选，2弹窗 |
| `fFileReadCheck` | tinyint |  |  | 否 | 0 |  |
| `fProjectList` | tinyint |  |  | 否 | 0 | 项目列表 0 无 1 有-独立数据 2 有-录标共享数据 |
| `fProjectListCheck` | tinyint |  |  | 否 | 0 |  |
| `fPolicyholder` | tinyint |  |  |  |  | 投保人信息，1、全部输入,存后1字段不可改；2、2字段取自中心不可改；3、3字段取自中心不可改，4、4字段取自中心不可改 |
| `fPolicyholderCheck` | tinyint |  |  | 否 | 0 |  |
| `fAccountInfo` | tinyint |  |  |  |  | 基本户信息，1需输入基本户，2无需输入基本户，3无-基本户前往中心修改 |
| `fAccountInfoCheck` | tinyint |  |  | 否 | 0 |  |
| `fSignType` | tinyint |  |  |  |  | 签章模式，1e签宝+企业认证，2CA签章（福建），3CA签章（温州翔晟） |
| `fSignCAType` | tinyint |  |  | 否 | 0 |  |
| `fSignTypeCheck` | tinyint |  |  | 否 | 0 |  |
| `fPayRecord` | tinyint |  |  |  |  | 支付记录，1有，2无 |
| `fPayRecordCheck` | tinyint |  |  | 否 | 0 | 支付记录，1有，2无 |
| `fAccountManage` | tinyint |  |  |  |  | 账户管理，1无，2有，手机+密码，3有，手机+密码+认证 |
| `fAccountManageCheck` | tinyint |  |  | 否 | 0 |  |
| `fServiceStyle` | tinyint |  |  |  | 1 | 客服样式 1.左侧底部 2.左侧整体(整个菜单内容去掉) |
| `fServiceStyleCheck` | tinyint |  |  | 否 | 0 |  |
| `fServiceShow` | tinyint |  |  |  | 0 | 客服电话显示 |
| `fServiceShowCheck` | tinyint |  |  | 否 | 0 |  |
| `fPageHeader` | tinyint |  |  | 否 | 1 | 详情页头部 1 显示步骤 2 显示保司名称 |
| `fPageHeaderCheck` | tinyint |  |  | 否 | 0 |  |
| `fOrderClose` | tinyint |  |  | 否 | 1 |  |
| `fCloseTip` | tinyint |  |  | 否 | 1 |  |
| `fOrderCloseCheck` | tinyint |  |  | 否 | 0 |  |
| `fFormPage` | tinyint |  |  | 否 | 1 |  |
| `CreateTime` | datetime |  |  |  |  |  |
| `fFormPageCheck` | tinyint |  |  | 否 | 0 |  |
| `cUserId` | nvarchar(50) |  |  |  |  |  |
| `fFrom` | tinyint |  |  | 否 |  | 来源（1：中心配置管理的高级搜索；2：客户端模式管理的高级搜索） |

## T_StateMent_Log

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `fFileId` | varchar(50) |  |  |  |  |  |
| `cPolicyNo` | varchar(50) |  |  |  |  | 保单号 |
| `cOwnerUnit` | nvarchar(100) |  |  |  |  | 业主单位名称 被保险人 |
| `cEnterpriseName` | nvarchar(100) |  |  |  |  | 保险人 |
| `tGuaranteedTime` | varchar(50) |  |  |  |  | 签单日期 |
| `tEffectiveTime` | varchar(50) |  |  |  |  | 生效日期 |
| `fPremium` | varchar(50) |  |  |  |  | 保费 |
| `fState` | nvarchar(10) |  |  |  |  | 状态值 |
| `CreateTime` | varchar(50) |  |  |  | getdate() |  |
| `cBz` | nvarchar(300) |  |  |  |  |  |
| `cBzTime` | varchar(20) |  |  |  |  |  |
| `fOrder` | int |  |  |  | 0 | 对应fState |

## T_XK_OrderContacts

*线客，联系人与订单关系表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `fContactsID` | int |  |  |  | 0 | 关联T_XK_Contacts表ID |
| `fOrderID` | int |  |  |  | 0 | 关联T_XK_Order表ID |
| `cCreateUser` | nvarchar(20) |  |  |  |  | 创建人 |
| `cCreateUserID` | nvarchar(50) |  |  |  |  | 创建人ID，关联user表ID |
| `fState` | tinyint |  |  |  | 0 | 有效状态，默认0无效，1有效 |
| `tUpdatetime` | datetime |  |  |  |  | 更新时间 |

## T_PProduct_DiversifiedFileTemplateBase

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fInsuranceID` | int |  |  | 否 | 0 | 保险公司ID |
| `cName` | nvarchar(50) |  |  |  |  | 附件模板名称 |
| `fIsDefault` | tinyint |  |  | 否 | 0 | 是否默认 0 否 1 是 |
| `tCreateTime` | datetime |  |  |  | getdate() |  |
| `fInsuranceTypeID` | int |  |  |  |  | 险种ID |
| `fSuperviseID` | int |  |  | 否 | 0 |  |

## T_ZX_Address

*振鑫担保小程序-用户地址信息表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `fZXUserID` | int |  |  |  | 0 | 关联T_ZX_User表ID |
| `cBName` | nvarchar(50) |  |  |  |  | 收货人姓名 |
| `fSex` | tinyint |  |  |  |  | 用户的性别，值为1时是男性，值为2时是女性， |
| `cPhone` | varchar(20) |  |  |  |  | 手机号码 |
| `cSheng` | nvarchar(30) |  |  |  |  | 省 |
| `cShengCode` | nvarchar(20) |  |  |  |  | 省对应的代码 |
| `cShi` | nvarchar(30) |  |  |  |  | 市 |
| `cShiCode` | nvarchar(20) |  |  |  |  | 市对应的代码 |
| `cQu` | nvarchar(30) |  |  |  |  | 区 |
| `cQuCode` | nvarchar(20) |  |  |  |  | 区对应的代码 |
| `cAddress` | nvarchar(50) |  |  |  |  | 详细地址，不包括省市区 |
| `fIsDefault` | tinyint |  |  |  | 0 | 是否默认，0否，1是 |
| `tCreateTime` | datetime |  |  |  | getdate() | 创建时间 |

## T_StateMent_Log2

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `fFileId` | varchar(50) |  |  |  |  |  |
| `cPolicyNo` | varchar(50) |  |  |  |  |  |
| `cOwnerUnit` | nvarchar(100) |  |  |  |  | 被保险人 |
| `fPremium` | varchar(50) |  |  |  |  | 实收保费 |
| `cFybl` | varchar(50) |  |  |  |  | 费用比例 |
| `cYsSxf` | varchar(50) |  |  |  |  | 应收手续费 |
| `cJsbl` | varchar(50) |  |  |  |  | 结算比列 |
| `cYjsFf` | varchar(50) |  |  |  |  | 已结收付费 |
| `cDjSxf` | varchar(50) |  |  |  |  | 待结手续费 |
| `cJsSj` | varchar(50) |  |  |  |  | 结算时间 |
| `CreateTime` | varchar(50) |  |  |  |  | 核对时间 |
| `fState` | varchar(50) |  |  |  |  | 状态 |
| `cBz` | nvarchar(300) |  |  |  |  | 备注 |
| `cBzTime` | varchar(20) |  |  |  |  | 备注时间 |
| `fOrder` | int |  |  |  |  | 对应fState |

## T_PProduct_ServeRisk

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cServerRiskID` | nvarchar(200) |  |  | 否 |  |  |
| `cServerDetailID` | nvarchar(200) |  |  |  |  |  |
| `cFileName` | nvarchar(200) |  |  |  |  | 附件名称 |
| `cFileUrl` | varchar(200) |  |  |  |  | 附件地址 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cServeNum` | varchar(50) |  |  |  |  | T_PProduct_Serve关联字段cServeNum |
| `cFileDesc` | nvarchar(500) |  |  |  |  | 整改附件描述 |

## T_Sys_Log

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `logKey` | nvarchar(50) |  |  | 否 |  |  |
| `logMessage` | nvarchar(MAX) |  |  |  |  |  |
| `tdate` | datetime |  |  | 否 | getdate() |  |
| `logTag` | nvarchar(50) |  |  |  |  |  |
| `logUrl` | varchar(300) |  |  |  |  | 请求地址 |

## T_PProduct_EmailLog

*履约发票邮件发送列表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `ID` | int | 是 | 是 | 否 |  |  |
| `emailTitle` | nvarchar(50) |  |  |  |  | 邮件标题 |
| `receiveAddress` | varchar(100) |  |  |  |  | 收件地址 |
| `xlsUrl` | varchar(200) |  |  |  |  | xls附件地址 |
| `zipUrl` | varchar(200) |  |  |  |  | zip附件地址 |
| `fstate` | tinyint |  |  |  | 0 | 0：未处理，1：已处理 |
| `tdate` | datetime |  |  |  |  | 添加时间 |
| `subdate` | datetime |  |  |  |  | 处理时间 |
| `cAuditUserName` | nvarchar(50) |  |  |  |  | 处理人姓名 |
| `platformcode` | varchar(50) |  |  |  |  | 平台编码 |
| `cInsuranceCompany` | nvarchar(50) |  |  |  |  | 承保机构 |
| `sendCode` | varchar(50) |  |  |  |  | 发件编号 |
| `fInsuranceTypeID` | int |  |  |  |  | 险种ID |
| `fInsuranceTypeCode` | nvarchar(50) |  |  |  |  | 险种编码 |
| `fInsuranceTypeName` | nvarchar(50) |  |  |  |  | 险种名称 |

## T_RbRuleName

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int |  | 是 | 否 |  |  |
| `cRuleName` | nvarchar(50) |  |  |  |  | 规则名称 |
| `cRuleContent` | nvarchar(100) |  |  |  |  | 规则内容 |
| `PRC_id` | int |  |  |  |  | T_PRC_Info.ID |
| `tdate` | datetime |  |  |  | getdate() | 创建日期 |
| `cRuleRemarks` | nvarchar(100) |  |  |  |  | 规则备注 |

## T_PrcOperation_Log

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cUser` | nvarchar(50) |  |  |  |  | 操作人 |
| `cLoginName` | nvarchar(50) |  |  |  |  | 登录名 |
| `cMenu` | nvarchar(50) |  |  |  |  | 菜单名称 |
| `cButton` | nvarchar(50) |  |  |  |  | 操作按钮名称 |
| `cPrc` | nvarchar(50) |  |  |  |  | 中心编码+名称 |
| `cOldContent` | nvarchar(MAX) |  |  |  |  | 原内容 |
| `cContent` | nvarchar(MAX) |  |  |  |  | 变更后的内容 |
| `tDate` | datetime |  |  |  | getdate() | 操作时间 |
| `cIP` | nvarchar(50) |  |  |  |  | 操作人IP |

## T_PProduct_ServeRiskAttachment

*风险附件表*

| 字段名 | 类型 | 主键 | 自增 | 可NULL | 默认值 | 说明 |
|--------|------|------|------|--------|--------|------|
| `id` | int | 是 | 是 | 否 |  |  |
| `cServerRiskID` | nvarchar(200) |  |  | 否 |  |  |
| `cServerDetailID` | nvarchar(200) |  |  |  |  |  |
| `cFileName` | nvarchar(200) |  |  |  |  | 附件名称 |
| `cFileUrl` | varchar(200) |  |  |  |  | 附件地址 |
| `tCreateTime` | datetime |  |  |  |  |  |
| `cServeNum` | varchar(50) |  |  |  |  | T_PProduct_Serve关联字段cServeNum |
