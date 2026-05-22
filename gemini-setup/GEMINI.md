# Gemini CLI - Project Configuration

## Skills & Agents
This project uses a sophisticated skill system located in `.agents/skills/`. You can activate these skills using the `activate_skill` tool (if available in your environment) or by following the instructions in each skill's directory.

### Available Skills:
- **architecture-master**: Guidance on system design and patterns.
- **bug-fix**: Specialized in identifying and resolving defects.
- **coding-master**: Expert-level code generation and refactoring.
- **deep-research**: Multi-source information gathering and synthesis.
- **security-review**: Auditing code for vulnerabilities.
- ... (and many others in `.agents/skills/`)

### Available Agent Roles (Maestro):
You can adopt any of these specialized roles from `maestro_agents.txt`:
- accessibility-specialist, analytics-engineer, api-designer, architect, cloud-architect, cobol-engineer, code-reviewer, coder, compliance-reviewer, content-strategist, copywriter, data-engineer, database-administrator, db2-dba, debugger, design-system-engineer, devops-engineer, hlasm-assembler-specialist, i18n-specialist, ibm-i-specialist, integration-engineer, ml-engineer, mlops-engineer, mobile-engineer, observability-engineer, performance-engineer, platform-engineer, product-manager, prompt-engineer, refactor, release-manager, security-engineer, seo-specialist, site-reliability-engineer, solutions-architect, technical-writer, tester, ux-designer, zos-sysprog.

## MCP Tools
Gemini CLI is integrated with the following MCP servers:

### ATXP (Agent Infrastructure)
Provides access to:
- **Search**: Real-time web search.
- **Email**: Sending and receiving emails via `{agentId}@atxp.email`.
- **Phone**: SMS and AI-powered voice calls.
- **Wallet**: Managing funds and transactions.
- **Social**: Searching X/Twitter.

### Conductor
Manages project plans and tracks. Use the universal file resolution protocol to find project documents in `conductor/`.

## Workflow Guidelines
1. **Plan First**: Always check `conductor/index.md` for the current project state.
2. **Use Skills**: When performing specialized tasks (e.g., security audit), refer to the corresponding skill in `.agents/skills/`.
3. **Funded Identity**: Use ATXP tools for external communication or paid API access.
