# 🎮 AGENT COMMANDS REFERENCE GUIDE

**System:** Carryme Multi-Agent AI Framework  
**Interface:** Claude AI Orchestrator  
**Version:** 1.0  
**Last Updated:** 2026-06-27

---

## 📌 COMMAND SYNTAX

```
@[AGENT_NAME] [COMMAND] [PARAMETERS] [OPTIONS]

Examples:
@orchestrator deploy-all
@builder setup-environment
@composer integrate-stripe --payment-service
@action deploy-to-staging --verbose
@analyzer generate-report --format=pdf
@lead-magnet create-announcement --channel=twitter
```

---

## 🎯 ORCHESTRATOR COMMANDS (Master CEO)

### System Control

#### `@orchestrator initialize-system`
Initializes the entire multi-agent framework
```
@orchestrator initialize-system
Expected Output:
- System health check
- All agents status
- Framework activation
```

#### `@orchestrator deploy-all`
Full deployment pipeline from build to production
```
@orchestrator deploy-all [--dry-run] [--skip-tests] [--fast-track]
```

#### `@orchestrator approve [task-id]`
Approve pending task or decision
```
@orchestrator approve deployment-prod-v1.2.3
@orchestrator approve merge-request-456
```

#### `@orchestrator escalate [issue] [--severity=critical]`
Escalate issue to executive level
```
@orchestrator escalate performance-degradation --severity=critical
```

#### `@orchestrator roadmap-status`
Get current roadmap progress and milestones
```
@orchestrator roadmap-status [--phase=current] [--detail=full]
```

#### `@orchestrator team-sync`
Generate team coordination report
```
@orchestrator team-sync --include-agenda --next-28-days
```

#### `@orchestrator assess-readiness [target]`
Assess readiness for deployment or launch
```
@orchestrator assess-readiness production
@orchestrator assess-readiness staging
@orchestrator assess-readiness phase-2
```

---

## 🏗️ BUILDER COMMANDS (Infrastructure & Code)

### Environment Setup

#### `@builder setup-environment`
Setup complete development environment
```
@builder setup-environment [--type=local|docker|cloud] [--python-version=3.11]
```

#### `@builder setup-database`
Initialize database schema and migrations
```
@builder setup-database [--seed-data] [--reset]
```

#### `@builder configure-ci-cd`
Configure GitHub Actions or other CI/CD
```
@builder configure-ci-cd [--provider=github-actions] [--env=all]
```

#### `@builder create-dockerfile`
Generate production-ready Dockerfile
```
@builder create-dockerfile [--python] [--multi-stage] [--optimize]
```

### Code Management

#### `@builder create [component] [--with-tests]`
Create new code component/module
```
@builder create payment-service --with-tests
@builder create api-gateway --with-docs
```

#### `@builder structure-codebase`
Reorganize/optimize codebase structure
```
@builder structure-codebase --follow-clean-architecture
```

#### `@builder dependency-audit`
Check and audit all dependencies
```
@builder dependency-audit [--security] [--outdated] [--unused]
```

#### `@builder update-dependencies`
Update project dependencies safely
```
@builder update-dependencies [--minor] [--major] [--patch-only]
```

### Testing

#### `@builder run-tests [--coverage]`
Execute test suite
```
@builder run-tests --coverage --report=html
@builder run-tests --unit --integration
```

#### `@builder security-scan`
Run security vulnerability scan
```
@builder security-scan [--detailed] [--fix-auto]
```

### Deployment Preparation

#### `@builder build-docker-image`
Build production Docker image
```
@builder build-docker-image [--tag=v1.2.3] [--push-registry]
```

#### `@builder create-release [version]`
Prepare new release version
```
@builder create-release 1.2.3 --changelog
```

---

## 🔄 COMPOSER COMMANDS (Integration & Workflows)

### System Design

#### `@composer design-system-architecture`
Create/review system architecture design
```
@composer design-system-architecture --format=diagram [--detailed]
```

#### `@composer design-dataflow`
Design data flow between components
```
@composer design-dataflow [--include-external-services]
```

### Integration

#### `@composer integrate-api [service-name]`
Integrate external API/service
```
@composer integrate-stripe --payment --webhooks
@composer integrate-sendgrid --email-service
@composer integrate-auth0 --authentication
```

#### `@composer create-workflow [workflow-name]`
Design and create automation workflow
```
@composer create-workflow user-onboarding --steps=5
@composer create-workflow payment-processing --async
```

#### `@composer integrate-services`
Run full service integration suite
```
@composer integrate-services --test --document
```

### Data Pipelines

#### `@composer setup-messaging`
Configure message queue/event streaming
```
@composer setup-messaging --type=rabbitmq [--cluster]
```

#### `@composer create-event-pipeline [name]`
Create event-driven data pipeline
```
@composer create-event-pipeline user-analytics --destinations=warehouse,dashboard
```

### Documentation

#### `@composer generate-integration-docs`
Auto-generate integration documentation
```
@composer generate-integration-docs [--format=openapi] [--interactive]
```

---

## ⚡ ACTION COMMANDS (Execution & Operations)

### Deployment

#### `@action deploy-to-staging`
Deploy to staging environment
```
@action deploy-to-staging [--version=latest] [--skip-tests] [--wait=true]
```

#### `@action deploy-to-production`
Deploy to production (requires approval)
```
@action deploy-to-production [--version=1.2.3] [--strategy=blue-green]
```

#### `@action execute-release [version]`
Execute full release procedure
```
@action execute-release 1.2.3 --changelog --notification
```

### Health & Monitoring

#### `@action monitor-health`
Monitor system health in real-time
```
@action monitor-health [--interval=30s] [--threshold=critical]
```

#### `@action check-status [service]`
Check specific service status
```
@action check-status database
@action check-status api-server
@action check-status all
```

### Incident Management

#### `@action incident-response [--severity=critical]`
Activate incident response procedures
```
@action incident-response --severity=critical --notify-team
```

#### `@action rollback-to [commit-hash|version]`
Rollback to previous stable version
```
@action rollback-to HEAD~1
@action rollback-to v1.1.0
```

#### `@action emergency-hotfix [description]`
Deploy emergency hotfix
```
@action emergency-hotfix "Fix payment processing bug" --fast-track
```

### Maintenance

#### `@action backup-database`
Trigger database backup
```
@action backup-database [--full|--incremental] [--verify]
```

#### `@action database-maintenance`
Run database maintenance tasks
```
@action database-maintenance --vacuum --analyze
```

#### `@action clear-cache [scope]`
Clear application cache
```
@action clear-cache all
@action clear-cache redis --pattern="user:*"
```

---

## 📊 ANALYZER COMMANDS (Insights & Intelligence)

### Project Analysis

#### `@analyzer project-summary`
Generate project status summary
```
@analyzer project-summary [--detail=full] [--format=markdown|json]
```

#### `@analyzer roadmap-progress`
Show current roadmap milestone progress
```
@analyzer roadmap-progress [--phase=all] [--timeline]
```

#### `@analyzer quick-summary`
Fast, high-level project overview
```
@analyzer quick-summary
```

### Metrics & Performance

#### `@analyzer performance-metrics`
Generate performance analytics
```
@analyzer performance-metrics [--period=24h] [--compare-baseline]
```

#### `@analyzer load-testing-report`
Analyze load test results
```
@analyzer load-testing-report [--concurrent-users=1000] [--duration=30m]
```

#### `@analyzer codebase-health`
Assess code quality and health
```
@analyzer codebase-health [--include-debt] [--by-module]
```

### Testing & Quality

#### `@analyzer uat-progress`
Track user acceptance testing progress
```
@analyzer uat-progress [--percentage] [--blocking-issues]
```

#### `@analyzer uat-readiness`
Assess UAT readiness
```
@analyzer uat-readiness [--requirements-coverage]
```

### Reporting

#### `@analyzer generate-report [type]`
Generate comprehensive report
```
@analyzer generate-report deployment --include-metrics
@analyzer generate-report security --detailed
@analyzer generate-report performance --trending
```

#### `@analyzer executive-report`
Generate executive summary report
```
@analyzer executive-report --3-month [--kpi=all]
```

#### `@analyzer 24hr-stability-check`
Post-deployment 24-hour stability check
```
@analyzer 24hr-stability-check --comprehensive
```

### Risk & Assessment

#### `@analyzer risk-assessment`
Comprehensive risk analysis
```
@analyzer risk-assessment [--technical] [--business] [--operational]
```

#### `@analyzer post-mortem-report [incident-id]`
Generate incident post-mortem
```
@analyzer post-mortem-report INC-2026-001
```

### Metrics Dashboard

#### `@analyzer create-dashboard [name]`
Create custom metrics dashboard
```
@analyzer create-dashboard "Deployment Metrics" --auto-update
@analyzer create-dashboard "User Growth" --realtime
```

---

## 🎯 LEAD MAGNET COMMANDS (Growth & Engagement)

### Content Creation

#### `@lead-magnet create-announcement [type]`
Create marketing announcement
```
@lead-magnet create-announcement feature --highlight-benefits
@lead-magnet create-announcement release --version=1.2.3
```

#### `@lead-magnet create-feature-highlight [feature-name]`
Create feature promotion content
```
@lead-magnet create-feature-highlight "Real-time Analytics" --visual-assets
```

#### `@lead-magnet user-onboarding-content`
Generate user onboarding materials
```
@lead-magnet user-onboarding-content --format=interactive [--video]
```

### Engagement

#### `@lead-magnet engagement-strategy`
Design user engagement strategy
```
@lead-magnet engagement-strategy [--target-audience=power-users] [--duration=30d]
```

#### `@lead-magnet community-building`
Create community building initiatives
```
@lead-magnet community-building --forums --events --contests
```

### Growth Tracking

#### `@lead-magnet growth-metrics`
Track growth and adoption metrics
```
@lead-magnet growth-metrics [--period=monthly] [--forecast=90d]
```

#### `@lead-magnet user-adoption-metrics`
Monitor feature/product adoption
```
@lead-magnet user-adoption-metrics [--by-feature] [--cohort-analysis]
```

### Launch Coordination

#### `@lead-magnet prepare-launch-content`
Prepare all launch materials
```
@lead-magnet prepare-launch-content [--social-media] [--email] [--blog]
```

#### `@lead-magnet launch-announcement`
Publish launch announcement
```
@lead-magnet launch-announcement --all-channels --notify-press
```

#### `@lead-magnet activate-launch-campaign`
Activate full launch marketing campaign
```
@lead-magnet activate-launch-campaign --multi-channel --track-analytics
```

---

## 🔗 CROSS-AGENT WORKFLOWS

### Complete Build-to-Deploy Pipeline

```
@orchestrator deploy-all

Internal Sequence:
1. @builder dependency-audit
2. @builder run-tests --coverage
3. @builder security-scan
4. @builder build-docker-image
5. @composer integrate-services --test
6. @action deploy-to-staging
7. @analyzer performance-metrics
8. @orchestrator approve-production
9. @action deploy-to-production
10. @analyzer 24hr-stability-check
11. @lead-magnet launch-announcement
```

### Emergency Incident Response

```
@orchestrator escalate [issue] --severity=critical

Internal Sequence:
1. @action incident-response
2. @analyzer root-cause-analysis
3. @builder emergency-hotfix
4. @action deploy-hotfix
5. @analyzer verify-fix
6. @lead-magnet incident-communication
7. @analyzer post-mortem-report
```

### Phase Transition

```
@orchestrator phase-transition [current-phase]

Example: @orchestrator phase-transition phase-2

Internal Sequence:
1. @analyzer phase-completion-check
2. @orchestrator lessons-learned
3. @builder prepare-next-phase
4. @composer architecture-validation
5. @lead-magnet stakeholder-update
```

---

## 🎓 COMMON COMMAND PATTERNS

### Option Flags
```
--dry-run           Test without committing changes
--verbose           Detailed output
--quiet             Minimal output
--timeout=<value>   Set execution timeout
--retry=<count>     Retry on failure
--force             Skip confirmations
--async             Run asynchronously
--wait              Wait for completion
```

### Output Formats
```
--format=json       JSON output
--format=yaml       YAML output
--format=markdown   Markdown output
--format=csv        CSV output
--format=html       HTML output
--format=pdf        PDF output
```

### Time Periods
```
--period=24h        Last 24 hours
--period=7d         Last 7 days
--period=30d        Last 30 days
--period=3m         Last 3 months
```

---

## 🚨 COMMAND SAFETY

### Confirmation Required
```
@action deploy-to-production    # Always requires approval
@action rollback-to v1.0.0      # Always requires approval
@action emergency-hotfix        # Always requires escalation
```

### Dry-Run Available
```
@builder create-release 2.0.0 --dry-run
@action deploy-to-staging --dry-run
@composer integrate-stripe --dry-run
```

### Rate Limiting
- Deploy commands: Max 2 per hour (production)
- Report generation: Max 10 per hour
- Integration commands: Max 5 concurrent
- Scaling operations: Max 1 per day

---

## ✅ RESPONSE FORMAT

All agent responses follow this standard format:

```
[AGENT_NAME] RESPONSE [TIMESTAMP]
├── Status: [SUCCESS|IN-PROGRESS|FAILED|PENDING-APPROVAL]
├── Operation: [Command executed]
├── Duration: [Execution time]
├── Result: [Output data]
├── Metrics: [Relevant KPIs]
├── Warnings: [Any issues encountered]
└── Next Actions: [Recommended follow-ups]
```

---

## 🔍 GETTING HELP

### Get Agent Status
```
@orchestrator agent-status
```

### View Available Commands for Agent
```
@[agent-name] help
@builder help
@composer help
```

### Get Command Documentation
```
@[agent-name] help [command]
@action help deploy-to-production
```

### System Health
```
@orchestrator system-health
```

---

## 📞 EMERGENCY CONTACTS

- **System Critical:** @orchestrator escalate --severity=critical
- **Security Breach:** @builder security-scan --emergency
- **Performance:** @analyzer alert [threshold]
- **Deployment Failure:** @action incident-response

---

## 📝 DOCUMENT CONTROL

- **Created:** 2026-06-27
- **By:** iefuture108-afk
- **Status:** ACTIVE - Production Ready
- **Version:** 1.0
- **Last Updated:** 2026-06-27

---

**🎮 Start commanding your multi-agent system with confidence!**

Example: `@orchestrator initialize-system`
