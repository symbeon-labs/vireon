# VIREON Licensing

VIREON uses a **dual-license model** to balance open-source collaboration with sustainable development.

---

## 📜 License Tiers

### Community Edition (MIT License)

**What's Included:**
- ✅ Python orchestration API (`vireon/core.py`, `vireon/models.py`)
- ✅ Configuration system (`vireon.yaml`)
- ✅ MCP client integration
- ✅ Up to **2 concurrent agents**
- ✅ Basic examples and documentation

**Limitations:**
- ⚠️ Limited agent count (2 maximum)
- ⚠️ No advanced governance features
- ⚠️ Community support only (GitHub Issues)

**License:** [MIT License](./LICENSE)  
**Cost:** Free forever

---

### Professional Edition (Commercial License)

**What's Included:**
- ✅ Everything in Community +
- ✅ Optimized Rust governance engine (binary only)
- ✅ Up to **10 concurrent agents**
- ✅ Custom governance rules
- ✅ Audit logging
- ✅ Email support (48h SLA)

**Limitations:**
- ⚠️ Single-machine license binding
- ⚠️ No source access to Rust core

**License:** Commercial - License key required  
**Cost:** $99/month per developer  
**Purchase:** [vireon.ai/pricing](https://vireon.ai/pricing) *(coming soon)*

---

### Enterprise Edition (Commercial License)

**What's Included:**
- ✅ Everything in Professional +
- ✅ **Unlimited agents**
- ✅ Air-gap deployment (on-premise)
- ✅ SOC2 compliance features
- ✅ Priority support (4h SLA)
- ✅ Custom contract terms
- ✅ Optional source code access (under NDA)

**License:** Commercial - Annual contract  
**Cost:** Starting at $499/month + per-seat fees  
**Contact:** enterprise@vireon.ai

---

## 🔐 Proprietary Components

The following components are **NOT open source** and are distributed as compiled binaries only:

```
core/sage_x_rust_module/lib/
├── libvireon_core.so       (Linux x86_64)
├── vireon_core.dll         (Windows x86_64)
└── libvireon_core.dylib    (macOS x86_64/ARM64)
```

**License:** © 2025 Symbeon Labs. All Rights Reserved.  
**Distribution:** Binaries may be redistributed only as part of VIREON packages.  
**Reverse Engineering:** Explicitly prohibited under DMCA and applicable laws.

**Source Code:** Available only under Enterprise agreements with signed NDA.

---

## ⚖️ Patents

Certain algorithms and methods used in VIREON may be covered by pending or issued patents:

- Multi-Agent Consensus with Hallucination Detection
- Adaptive Governance for LLM Orchestration
- Zero-Trust Context Sharing in Distributed AI

**Patent Holder:** Symbeon Labs  
**Status:** Provisional applications filed (2025)

Users of Community and Professional editions receive a **royalty-free license** for non-commercial and internal commercial use.

**Competitive Use:** Building a competing orchestration platform using VIREON's patented methods requires a separate licensing agreement.

---

## 🆓 Free Use Cases

VIREON Community Edition is **free to use** for:

✅ Personal projects  
✅ Academic research  
✅ Open-source projects  
✅ Internal tools (non-redistributed)  
✅ Prototyping and evaluation

**No license key needed** for Community tier.

---

## 🔑 How to Activate a License

### Step 1: Set Environment Variable

```bash
# Linux/macOS
export VIREON_LICENSE_KEY="VIREON-PRO-XXXXXXXXXXXX"

# Windows PowerShell
$env:VIREON_LICENSE_KEY="VIREON-PRO-XXXXXXXXXXXX"

# Or add to .env file
echo 'VIREON_LICENSE_KEY=VIREON-PRO-XXXXXXXXXXXX' >> .env
```

### Step 2: Verify Activation

```python
from vireon.licensing import get_validator

validator = get_validator()
result = validator.validate()

print(f"Tier: {result['tier']}")
print(f"Max Agents: {result['max_agents']}")
print(f"Features: {result['features']}")
```

### Step 3: Start Orchestrating

```python
from vireon import VireonCore

vireon = VireonCore(config="./vireon.yaml")

# This will now work with up to 10 agents (Professional)
# or unlimited (Enterprise)
result = await vireon.swarm_execute(
    task="Your task here",
    agents=["agent1", "agent2", ..., "agent10"]
)
```

---

## 📞 Contact & Support

### Community Support
- GitHub Issues: [github.com/symbeon-labs/vireon/issues](https://github.com/symbeon-labs/vireon/issues)
- Discussions: [github.com/symbeon-labs/vireon/discussions](https://github.com/symbeon-labs/vireon/discussions)

### Commercial Support
- Email: support@vireon.ai
- Response Time: 48h (Professional), 4h (Enterprise)

### Sales & Licensing
- Email: sales@symbeon.com
- Website: vireon.ai *(coming soon)*

---

## ❓ FAQ

**Q: Can I use VIREON Community in my startup?**  
A: Yes! As long as you stay within the 2-agent limit, it's free.

**Q: What happens if I exceed the agent limit?**  
A: The orchestration will fail with a license validation error prompting you to upgrade.

**Q: Can I buy a lifetime license?**  
A: Enterprise customers can negotiate perpetual licenses.

**Q: Is the Rust source code available?**  
A: Only to Enterprise customers under NDA. Community/Pro receive binaries only.

**Q: Can I self-host without internet for license validation?**  
A: Professional: Limited (cached validation for 24h). Enterprise: Yes (fully air-gapped).

---

**Last Updated:** 2025-12-08  
**Version:** 0.2.0-alpha
