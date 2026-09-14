# ARB-TOA-003A.6.2 — Internal TT lock

**Status.** Angular block convention-split locked. Explicit composite identified. Convention I evaluated.

**Scope.** Flat-slice circular-polarization control model, \(k\to 0\), \(\hat p=-\hat q\). No radial integral, no counterterm coefficients, no transfer claim.

---

## Relation to the fine-combed note

The fine-combed revision is algebraically correct under its stated 3D isotropy and internal-TT assumptions. Its editorial repairs (index notation, \(\langle\cdot\rangle_\Omega\), external-versus-internal distinction, double-trace diagnostic, two-convention split) stand.

What that note still lists as a recomputation order is now executed. The result is stronger than a consistency warning: the published pair is the exact isotropic average of one explicit non-TT composite, and the internal-TT projection of that composite vanishes.

---

## Locked composite

Helicity-2 polarizations on a right-handed frame \((\hat e_1,\hat e_2,\hat q)\):

\[
\hat m_\pm(\hat q)=\frac1{\sqrt2}(\hat e_1\pm i\hat e_2),\qquad
\varepsilon^\pm_{ij}(\hat q)=\hat m_{\pm i}\,\hat m_{\pm j}.
\]

Each \(\varepsilon^s(\hat q)\) is symmetric, traceless, and transverse to \(\hat q\).

The unique bilinear that reproduces the published coefficients is the index-contracted symmetrized product

\[
M_{ab}^{s_1s_2}(\hat q,\hat p)
=\varepsilon^{s_1}{}_{c(a}(\hat q)\;
\varepsilon^{s_2}{}_{b)}{}^{c}(\hat p).
\]

Visible symmetry: \(M_{ab}=M_{ba}\). Trace and transversality are *not* built in.

Under a right-handed frame at \(-\hat q\),

\[
\varepsilon^+(-\hat q)=-\varepsilon^-(\hat q)
\]

up to a unit phase that drops out of \(\mathscr E\).

---

## Pointwise identities at \(\hat p=-\hat q\)

Same-helicity products vanish (\(\hat m_\pm\cdot\hat m_\pm=0\)).

Opposite-helicity products collapse onto the transverse projector \(P_{ab}=\delta_{ab}-\hat q_a\hat q_b\):

\[
M_{ab}^{+-}=\frac12 P_{ab},\qquad
M^a{}_a^{+-}=1\neq 0,\qquad
\hat q^a M_{ab}=0.
\]

So \(M\) is symmetric and transverse, and is **not** traceless. It is a helicity-0 tensor in the plane \(\perp\hat q\). Convention I (Cotton-valued / internally TT \(M\)) already fails at step 2 of the recommended order.

Helicity sum:

\[
\mathscr E_{abcd}(\hat q,-\hat q)
=\sum_{s_1,s_2}M_{ab}^{s_1s_2}M_{cd}^{s_1s_2*}
=\frac12 P_{ab}P_{cd}.
\]

Spherical average with \(\langle\hat q_i\hat q_j\hat q_k\hat q_l\rangle=\frac1{15}(\delta_{ij}\delta_{kl}+\delta_{ik}\delta_{jl}+\delta_{il}\delta_{jk})\) yields

\[
\langle\mathscr E_{abcd}\rangle_\Omega
=\frac15\delta_{ab}\delta_{cd}
+\frac1{30}\bigl(\delta_{ac}\delta_{bd}+\delta_{ad}\delta_{bc}\bigr).
\]

This is the published pair, exactly:

\[
A=\frac15,\qquad B=\frac1{30},\qquad
3A+2B=\frac23,\qquad
2B=\frac1{15},\qquad
\langle\mathscr E^{ab}{}_{ab}\rangle_\Omega=1.
\]

The residual trace \(\frac23\delta_{cd}\) is the average of \(P_{cd}\), not a numerical artifact.

---

## Convention I after internal STT projection

\[
(S_\perp M)_{ab}
=P_a{}^c M_{cd}P^d{}_b-\frac12(\operatorname{tr}PM)\,P_{ab}.
\]

Since \(M\parallel P\), \(S_\perp M=0\) pointwise. The helicity-summed projected composite vanishes identically:

\[
A_{\mathrm{TT}}=B_{\mathrm{TT}}=0,\qquad
\varepsilon^{ab}\langle\mathscr E_{abcd}\rangle_\Omega\varepsilon^{cd}=0.
\]

The constraint \(3A+2B=0\) holds trivially. There is no remaining one-parameter TT family to normalize: \(\lambda=0\).

The external-TT contraction \(2B=\frac1{15}\) is therefore **not protected**. It is the contraction of the raw helicity-0 sector \(P_{ab}P_{cd}/2\). Internal TT removes that sector completely at this kinematic point.

---

## Convention table (replaces the open split)

| | Convention I — \(M\) Cotton / internal TT | Convention II — raw symmetrized product |
|---|---|---|
| \(M^a{}_a\) at \(\hat p=-\hat q\) | Must vanish. Does not, before projection. | Nonzero, \(=1\) on the opposite-helicity pair. |
| After \(S_\perp\) inside the sum | \(\mathscr E=0\) | Not applied |
| \((A,B)\) | \((0,0)\) | \(\bigl(\tfrac15,\tfrac1{30}\bigr)\) |
| External contact | \(0\) | \(\tfrac1{15}\) |
| Counterterm sector | No leading isotropic contact from this block | Trace sector required; \(C^2_\Sigma\) is not enough |
| Language allowed | “Cotton composite” | Must not be called Cotton on the internal indices |

The two conventions remain incompatible. The fine-combed note’s prohibition on mixing them is unchanged. What is new is that Convention I is no longer a pending recomputation: it evaluates to zero.

---

## What the fine-combed algebra still gets right

- Internal TT is pointwise on each \(M_{ab}^{s_1s_2}\), not a post-average condition.
- After averaging, the internally TT isotropic family is one-dimensional, spanned by \(S_{ab,cd}\), with \(A=-\frac23 B\).
- The fixed-axis projector averages to \((A,B)=\bigl(-\frac2{15},\frac15\bigr)\), ratio \(-\frac23\), distinct from the published ratio \(6\).
- Fixed-axis transversality need not survive \(\int\mathrm d\Omega_q\). Tracelessness must.
- External contraction with a unit ST tensor equals \(2B\) and is blind to \(A\).
- Double trace \(3A+12B=1\) diagnoses a raw normalization, consistent with Convention II.

---

## Ledger lines to change

- Angular coefficients \(A=\frac15\), \(B=\frac1{30}\): lock as **Convention II only**, with the explicit \(M\) above.
- TT contact \(\frac1{15}\): lock as **Convention II only**.
- Add: Convention I, same kinematics, same \(M\) after \(S_\perp\), contact \(=0\).
- The stronger claim that the isotropic \(q^{12}\) core vanishes is **true under Convention I** and **false under Convention II**.
- Radial UV degree, finite-\(k\) kernel, counterterm coefficients, and the nonlocal remainder stay gated.
- Closing criterion unchanged: only a finite, regulator-independent, nonlocal remainder that survives counterterm, basis, gauge, and state redefinitions can support a physical transfer claim.

---

## Next legitimate step

Not another isotropic \(k\to 0\) average. The finite-\(k\) kernel with \(\hat p=\widehat{\mathbf k-\mathbf q}\), under a declared convention (I or II, not both), then mode normalization and counterterm matching.
