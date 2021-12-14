from sgnlp.models.csgec import (
    CsgConfig,
    CsgModel,
    CsgTokenizer,
    CsgecPreprocessor,
    CsgecPostprocessor,
    download_tokenizer_files,
)

config = CsgConfig.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/csgec/config.json"
)
model = CsgModel.from_pretrained(
    "https://storage.googleapis.com/sgnlp/models/csgec/pytorch_model.bin",
    config=config,
)
download_tokenizer_files(
    "https://storage.googleapis.com/sgnlp/models/csgec/src_tokenizer/",
    "csgec_src_tokenizer",
)
download_tokenizer_files(
    "https://storage.googleapis.com/sgnlp/models/csgec/ctx_tokenizer/",
    "csgec_ctx_tokenizer",
)
download_tokenizer_files(
    "https://storage.googleapis.com/sgnlp/models/csgec/tgt_tokenizer/",
    "csgec_tgt_tokenizer",
)
src_tokenizer = CsgTokenizer.from_pretrained("csgec_src_tokenizer")
ctx_tokenizer = CsgTokenizer.from_pretrained("csgec_ctx_tokenizer")
tgt_tokenizer = CsgTokenizer.from_pretrained("csgec_tgt_tokenizer")

preprocessor = CsgecPreprocessor(
    src_tokenizer=src_tokenizer, ctx_tokenizer=ctx_tokenizer
)
postprocessor = CsgecPostprocessor(tgt_tokenizer=tgt_tokenizer)
