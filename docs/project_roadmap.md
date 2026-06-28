# Project Roadmap

## Project ATLAS — Route Resilience
### Bharatiya Antariksh Hackathon 2026 (ISRO) — PS-4

---

> ⚠️ **Status**: Roadmap Version 1.0 - Pending Official Video Validation
> *Do not modify this roadmap further until the official explanation video has been analyzed.*

---

## 🚩 Project Roadmap: Milestone 1

### **Name: System Architecture & End-to-End Mock Pipeline**
**Target Phases**: Phase 4 (Requirement Verification), Phase 5 (Architecture), Phase 6 (Documentation)

The goal of Milestone 1 is to finalize the blueprint of the system and establish the foundational communication between all modules, before any heavy mathematical or AI logic is written.

↓

### **Deliverables**
1. **Architecture Specifications**: 
   - High-Level Architecture (HLD) diagram.
   - Low-Level Architecture (LLD) detailing class structures.
   - Formal Data Flow diagram.
2. **API Contracts**: 
   - OpenAPI/Swagger definitions for the Backend to Frontend communication.
3. **Hero City Definition**: 
   - Exact geographical bounding box for the pre-computed Bengaluru dataset.
4. **Mock Pipeline Implementation**: 
   - A skeleton Backend that serves static, hardcoded JSON graph data.
   - A skeleton Frontend/Dashboard that successfully renders this static data.

↓

### **Acceptance Criteria**
- [ ] **Traceability**: Every architectural component traces back to the Requirement Traceability Matrix (REQ-01 to REQ-12).
- [ ] **Decoupling**: Graph processing is strictly decoupled from the live API (addressing TD-0001).
- [ ] **Data Contract**: Frontend successfully renders a static mock graph provided by the Backend API without UI blocking.
- [ ] **Documentation**: All architecture documents in the `architecture/` directory are marked "Approved".

↓

### **Review Gate: Architecture Review Board (ARB)**
Before moving to Milestone 2, the system must pass a formal Architecture Review using the `templates/architecture_review_template.md`. 
**Review Focus**: 
- Data pipeline bottlenecks.
- Scalability of the interactive dashboard.
- Viability of the AI-to-Graph conversion pipeline.

↓

### **Next Milestone: Milestone 2**
**Name: AI Baseline & Graph Construction Engine**
*(Targeting Phase 7 and Phase 8)*
- Training the baseline topology-aware AI model.
- Implementing the MST gap-bridging heuristic.
- Vectorizing masks into NetworkX graphs.
