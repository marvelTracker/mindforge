## 🧩 1. Token IDs → no meaning

**HOW:**

- Text → tokenizer splits into tokens
- Each token → integer index from vocabulary

```text
"novel" → 19384
```

**WHAT it does:**

- Converts text → discrete machine-readable symbols

**WHY needed:**

- Neural networks only work with numbers
- Fixed vocabulary enables efficient lookup

**KEY REMEMBER:**
👉 ID is just a pointer, not meaning

---

## 🧠 2. Embeddings → learned starting meaning

**HOW:**

- Token ID → row lookup in embedding matrix

```text
embedding = EmbeddingMatrix[token_id]
```

- Matrix is trained via gradient updates during training

**WHAT it does:**

- Converts token → dense vector (e.g., 4096 dims)

**WHY needed:**

- Enables semantic similarity:
  - similar words → similar vectors

**KEY REMEMBER:**
👉 Same token = same base vector
👉 Still context-free

---

## 📍 3. Positional encoding → inject order

**HOW:**

- Add position vector to embedding

```text
x = embedding + position_vector
```

- Could be sinusoidal / learned / RoPE

**WHAT it does:**

- Encodes token order + distance

**WHY needed:**

- Attention alone ignores order
- Language meaning depends on sequence

**KEY REMEMBER:**
👉 Same words + different order → different meaning

---

## 🔍 4. Attention → find relevance

**HOW:**

- Project tokens into Q, K

```text
Q = XW_Q
K = XW_K
```

- Compute similarity:

```text
scores = Q × Kᵀ
```

**WHAT it does:**

- Measures how much each token should attend to others

**WHY needed:**

- Identify important context

**KEY REMEMBER:**
👉 “Who matters to me?”

---

## ⚖️ 5. Softmax → normalize importance

**HOW:**

```text
weights = softmax(scores)
```

**WHAT it does:**

- Converts scores → probabilities (sum = 1)

**WHY needed:**

- Stable weighting of influence

**KEY REMEMBER:**
👉 Turns relevance → usable weights

---

## 🔄 6. Value mixing → build context meaning

**HOW:**

- Compute V:

```text
V = XW_V
```

- Weighted sum:

```text
Z = weights × V
```

**WHAT it does:**

- Combines information from relevant tokens

**WHY needed:**

- Actually transfer context information

**KEY REMEMBER:**
👉 Meaning = mixture of other tokens

---

## 🧠 7. Multi-head attention → multiple views

**HOW:**

- Run multiple Q/K/V projections in parallel
- Concatenate results

**WHAT it does:**

- Captures different relationships simultaneously

**WHY needed:**

- Language has multiple patterns:
  - syntax
  - semantics
  - long-range dependencies

**KEY REMEMBER:**
👉 Many “perspectives” at once

---

## ➕ 8. Residual + normalization → stabilize

**HOW:**

```text
X = X + AttentionOutput
X = LayerNorm(X)
```

**WHAT it does:**

- Preserves original info + stabilizes values

**WHY needed:**

- Prevents information loss
- Enables deep networks

**KEY REMEMBER:**
👉 Don’t overwrite—refine

---

## 🔧 9. FFN → deepen understanding

**HOW:**

```text
FFN(x) = W2 * activation(W1 * x)
```

**WHAT it does:**

- Nonlinear transformation per token

**WHY needed:**

- Build higher-level features
- Combine patterns learned from attention

**KEY REMEMBER:**
👉 Attention = gather
👉 FFN = process

---

## 🔁 10. Layer stacking → refine meaning

**HOW:**

- Repeat attention + FFN blocks many times

**WHAT it does:**

- Gradually builds abstraction

**WHY needed:**

- One pass isn’t enough for deep understanding

**KEY REMEMBER:**
👉 Meaning evolves layer by layer

---

## 🎯 11. Output projection → predict next token

**HOW:**

```text
logits = h_last × W_vocab
probs = softmax(logits)
```

**WHAT it does:**

- Converts final vector → probabilities over vocabulary

**WHY needed:**

- Model’s goal = next token prediction

**KEY REMEMBER:**
👉 Everything leads to this

---

## 🔁 12. Autoregressive loop → generate text

**HOW:**

- Append predicted token
- Repeat full pipeline

**WHAT it does:**

- Builds response token by token

**WHY needed:**

- Language generation is sequential

**KEY REMEMBER:**
👉 Think “one token at a time”

---

## 🏋️ 13. Training → adjusts weights using data

**HOW:**

```text
Forward pass → loss → backprop → update weights
```

**WHAT it does:**

- Improves predictions over time

**WHY needed:**

- Learn patterns from massive datasets

**KEY REMEMBER:**
👉 Data shapes weights, not stored directly

---

## 🧠 14. Final model → stores patterns, not data

**HOW:**

- All learned info encoded in:
  - embeddings
  - attention weights
  - FFN weights
  - output layer

**WHAT it does:**

- Acts as function:

```text
f(context) → next-token probabilities
```

**WHY needed:**

- Generalize to unseen inputs

**KEY REMEMBER:**
👉 Knowledge = distributed in weights

---

# ⚡ Ultra-short recall version (exam mode)

If you need a **10-second recall**:

```text
Text → tokens → embeddings → +position
→ attention (Q,K,V → weights → mix)
→ FFN → repeat layers
→ final vector → softmax → next token
→ loop

Training: adjust weights
Model: stores patterns, not data
```
