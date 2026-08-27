Dear Editors of *Behavior Research Methods*,

I am submitting **"Three Ways an Elicited Evaluation Measures Its Own Design"** for consideration
as an Article.

A large and growing class of studies asks a language model to report a number about a statement
— a confidence, a rating, a degree of some property — and then treats that number as a
measurement. Verbalized confidence, LLM-as-judge scoring, self-critique and most bespoke probes
built for a single paper all share this design. The paper measures three ways in which the
design produces the number as much as the model does, and converts each into a rule an author
can apply before collecting data.

The three quantities are measured on a common corpus of 7,920 elicitations across six frontier
model families, and then measured again on a second construct family built for this paper and
sharing no content with the first. That replication is the part I would most like reviewers to
weigh. It shows that **no magnitude transfers intact**: the item count needed for a ±0.05
half-width moves from 69 to 20 across domains, the threshold effect grows from a factor of 2 to
a factor of 16, and the instruction-framing effect does not replicate at all. The
non-replication is reported as a finding rather than smoothed over, because it identifies what
the effect depends on — framing is worth what the model could not have inferred without it.

**Why *Behavior Research Methods*.** The paper is psychometrics applied to a new kind of
respondent. Its content is between-item variance, the number of items needed for a target
interval, the reliability of a coefficient computed over raters, and the effect of
administration format on the response. Those are BRM's questions, and the journal's readership
is the one that will actually apply the rules rather than cite them in passing. I know of no
other venue where a paper whose contribution is "measure these three things before you report a
rate" is read as a contribution rather than as a caveat.

**Prior and overlapping work, stated plainly.** The first of the two construct families was
collected for two companion studies of a four-valued logic, co-authored with F. Smarandache and
submitted to the AAAI 2026 Fall Symposium Series; one of them is also a public preprint
(Preprints.org 230332). This manuscript is a methods paper and makes no claim about that logic,
which appears only as a worked example. Its own contributions — the three magnitudes measured on
a common corpus, the design rules, the nested ablation protocol, and the entire second construct
family with its 1,800 new elicitations — appear in neither companion. Where a number comes from
a companion paper the text says so, including the published figure of 0.661 that this manuscript
reports does not survive a larger item sample. I would rather the editors weigh this openly at
submission than discover it later.

**Data, code and materials.** Both item banks, all 7,920 raw generations including response
text, the elicitation and analysis scripts, and the code producing every figure and table are
public at https://github.com/mleyvaz/elicited-evaluation-design under MIT (code) and CC BY 4.0
(banks and generations). The repository deliberately includes the *first* version of one
analysis script, unrepaired: it took a high-confidence rate as the primary outcome, and that
choice turned out to be the very artifact the third result predicts. The sequence between the
two scripts is part of the evidence, and replacing the first quietly would have removed it.

The study involved no human or animal participants: every observation is a text generation
produced by a commercial model through a programmatic interface. The manuscript is not under
consideration elsewhere, and all listed material is original to it.

Thank you for your consideration.

Maikel Y. Leyva-Vázquez
Universidad Bernardo O'Higgins, Santiago, Chile
Universidad Bolivariana del Ecuador, Guayaquil, Ecuador
Universidad de Guayaquil, Guayaquil, Ecuador
myleyvav@ube.edu.ec · ORCID 0000-0001-7911-5879
