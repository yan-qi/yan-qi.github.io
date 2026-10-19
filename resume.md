---
layout: page
title: Resume
permalink: /resume/
---

## Yan Qi

**Senior Engineering Leader · Data Platform & Infrastructure Architecture · Distributed Systems**

Cupertino, CA · [yan.qi.asu@gmail.com](mailto:yan.qi.asu@gmail.com) · [linkedin.com/in/qiyan](https://www.linkedin.com/in/qiyan/)

**[Download PDF](/public/Yan_Qi_Resume.pdf)**

---

## Executive Summary

Senior Engineering Leader with **15+ years** building large-scale data platforms and distributed infrastructure, including **5+ years leading geo-distributed engineering teams** at Apple, Turn Inc., and Teradata. Deep expertise in business-critical content and event data platforms, real-time streaming architectures, distributed NoSQL storage, and production Generative AI integration.

Track record of global live-streaming launches, org-wide infrastructure cost reclamation, and building high-velocity engineering teams across time zones. Ph.D. in Computer Science, specializing in Database Systems and Query Optimization.

---

## Professional Experience

### Apple Inc. · Cupertino, CA

#### Senior Engineering Manager · 2021 – Present
*Data Platform & Infrastructure — Apple TV+ & Sports*

Lead a geo-distributed engineering team across Cupertino and Seattle responsible for the core content catalog metadata platform, live event data pipelines, and real-time analytics infrastructure powering Apple TV+, Apple Sports, and partner streaming ecosystems.

**Engineering Leadership & Team Development**

- **Org & Ownership:** Lead a team of up to 9 engineers plus contractors; own platform SLAs, on-call rotation, and incident accountability across a portfolio of business-critical production datasets.
- **Talent Growth:** Recruited, onboarded, and mentored engineers across two sites; developed and sponsored six engineers through promotion (two to staff level, four to senior level); grew an engineer into a technical-leadership role owning a major platform upgrade; managed a structured performance development plan through to measurable improvement.
- **Engineering Culture, Measured:** Instituted review and quality standards sustaining 100% code-review compliance, 93%+ test coverage, and zero production escapes over rolling 30-day windows.
- **Operating Model:** Own the team's technical roadmap and quarterly planning cycle; established the weekly operating rhythm (standup, backlog grooming, release gating, technical deep-dives) and async-first practices enabling cross-timezone delivery; built a self-service documentation and dependency-graph portal that cut ad-hoc stakeholder support load.
- **Cross-Org Influence:** Led a privacy-preserving analytics initiative spanning Privacy, Commerce, BI, Instrumentation, and QA teams through to approved production launch; sustained a multi-year partnership with the primary downstream consumer org on shared schema design.

**Platform Architecture & Cross-Org Impact**

- **Business-Critical Global Sports Infrastructure (Formula 1, MLS, MLB):**
  - Directed the end-to-end data platform build for the organization's largest and most complex global sports launch (F1 on Apple TV) — multi-canonical metadata, concurrent multi-view streams, and novel content-navigation features, delivered in a single quarter.
  - Supported the debut race weekend with **zero data pipeline outages** and all SLAs met.
  - Led delivery of real-time ingestion pipelines for Major League Soccer and Friday Night Baseball, bringing live event telemetry into near-real-time dashboards.
- **Unified Cross-Org Data Service Layer:**
  - Delivered an automated live-sports metadata service adopted as the shared content/data layer by multiple partner engineering teams, replacing per-team bespoke ingestion with a single governed source.
- **Next-Gen Aggregation Platform:**
  - Led the design of a query-time aggregation platform built on HyperLogLog probabilistic sketches, replacing rigid pre-computed OLAP cubes with on-the-fly computation.
  - Achieved an **order-of-magnitude reduction in stored data volume, >90% query runtime reduction, and >90% compute cost savings** across core datasets.
- **Enterprise Lakehouse Modernization & Cost Governance:**
  - Led a multi-quarter legacy batch pipeline deprecation and migration to a modern lakehouse platform across 5 core domain datasets, reclaiming **thousands of compute core-hours and terabyte-scale cluster storage** while eliminating years of accumulated pipeline tech debt.
  - Established cost attribution and chargeback modeling across shared data infrastructure consumed by multiple service teams, plus automated capacity planning that cut over-provisioning.
- **First Production Generative AI Integration:**
  - Led the team that delivered the organization's first production LLM-embeddings integration: semantic title matching that reconciles external partner reporting data against internal catalog records.
  - Raised automated match accuracy from a **~60% baseline to 94%** and cut report generation from 1–2 hours to under 10 minutes.
- **Cloud-Native Resilience:** Directed containerization and Kubernetes migration of mission-critical services with automated autoscaling and right-sizing, enabling zero-downtime deployments.

#### Engineering Manager · 2019 – 2021
*Content Analytics & Media Data Platform — Apple TV+ & Fitness+*

Led engineering teams delivering analytics infrastructure, real-time dashboards, and data pipelines for the global launch of Apple TV+ and Apple Fitness+.

- **Launch Data Infrastructure for Apple TV+:**
  - Led a new content-analytics platform from inception to production, enabling cross-functional executive visibility into content performance.
  - Delivered the organization's first Near-Real-Time streaming analytics engine on Spark and Kafka, with sub-minute metric freshness for live content dashboards.
- **Apple Fitness+ & Partner Ingestion:**
  - Delivered end-to-end data pipelines for Fitness+ catalog ingestion and partner reporting.
  - Sustained launch-window SLAs during major global product launches while expanding the team through targeted, diverse hiring.

#### Software Engineer · 2016 – 2019
*Media Products Data Platform (App Store, Music, TV, Podcasts, Books)*

Core architectural contributor to foundational data services across Apple Media Products.

- Built and operated petabyte-scale distributed storage and search infrastructure (Apache Cassandra, HBase, Solr/Lucene) serving content metadata and full-text catalog discovery to global client applications; contributed to migrating legacy batch infrastructure to Apache Spark and cloud-native architectures.

### Turn Inc. (Acquired by Amobee / Singtel) · Redwood City, CA

#### Architect, Scalable Data Platform · 2011 – 2016
*Scalable Data Platforms & AdTech Infrastructure*

Led architecture and core data engineering for a high-volume real-time bidding (RTB) and ad-targeting data platform.

- Architected **petabyte-scale** data lakes and ultra-low-latency stream processing for high-volume RTB traffic, plus distributed NoSQL and columnar analytical stores with multi-datacenter HA replication supporting continuous global ad serving and real-time attribution analytics.

### Teradata Corporation · San Diego, CA

#### Software Engineer, Advanced Development · 2009 – 2011
*Advanced Database Engine & Query Optimization*

Researched and implemented core engine features in Teradata's flagship massively parallel processing (MPP) data warehouse: next-generation columnar storage and cost-based distributed query optimization at multi-terabyte scale.

---

## Education

**Ph.D. in Computer Science** · Arizona State University, Tempe, AZ · 2004 – 2009
*Focus:* Cost-based query optimization in distributed and massively parallel databases, columnar indexing, and high-performance stream processing.

---

## Technical Skills

- **Platform & Big Data:** Apache Spark, Apache Flink, Apache Kafka, Apache Iceberg, Snowflake, Delta Lake, Trino/Presto, HyperLogLog aggregation
- **Distributed Storage & NoSQL:** Apache Cassandra, HBase, Solr / Lucene, PostgreSQL, columnar MPP engines
- **Cloud & Infrastructure:** Kubernetes, Docker, CI/CD, Grafana, multi-region deployments, capacity planning
- **AI / ML & LLM Engineering:** LLM embeddings & semantic matching, RAG, agentic AI systems, Vision-Language Models, vector databases
- **Programming Languages:** Java, Scala, Python, SQL, C++, Swift, TypeScript
- **Leadership & Governance:** Multi-site team leadership (Cupertino/Seattle), technical roadmap & quarterly planning, hiring & performance management, data governance, schema & lineage, cost attribution, incident management, GDPR/privacy compliance

---

## Certifications

Agentic AI & AI Agents for Leaders (Vanderbilt, 2025) · Generative AI Leadership & Strategy (Vanderbilt, 2024) · Deep Learning (DeepLearning.AI, 2023)
