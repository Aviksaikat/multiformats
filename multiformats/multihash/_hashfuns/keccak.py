"""
    Implementation for the ``keccak`` hash functions, using the optional dependency `safe-pysha3 <https://github.com/5afe/pysha3>`_.
"""

import hashlib
from typing import Optional

from multiformats.varint import BytesLike
from .utils import Hashfun, validate_hashfun_args

def _keccak(digest_bits: int) -> Hashfun:
    try:
        import sha3 # type: ignore # pylint: disable = import-outside-toplevel
    except ImportError as e:
<<<<<<< HEAD
        raise ImportError(
            "Module 'sha3' must be installed to use 'keccak' hash functions. Consider running 'pip install safe-pysha3'."
        ) from e
||||||| e9410e4 (fix: resolve incompatibility with typing-extensions >= 4.6.0. dependency changed to Aviksaikat/typing-validation.)
        raise ImportError(
            "Module 'sha3' must be installed to use 'keccak' hash functions. Consider running 'pip install pysha3'."
        ) from e
=======
        raise ImportError("Module 'sha3' must be installed to use 'keccak' hash functions. Consider running 'pip install pysha3'.") from e
>>>>>>> parent of e9410e4 (fix: resolve incompatibility with typing-extensions >= 4.6.0. dependency changed to Aviksaikat/typing-validation.)
    h = getattr(sha3, f"keccak_{digest_bits}")
    def hashfun(data: BytesLike, size: Optional[int] = None) -> bytes:
        validate_hashfun_args(data, size, digest_bits//8)
        m: hashlib._Hash = h() # pylint: disable = no-member
        m.update(data)
        d = m.digest()
        return d if size is None else d[:size]
    return hashfun

def _jit_register_keccak(m, register) -> bool: # type: ignore
    digest_bits = int(m[1])
    if register is not None:
        register(f"keccak-{digest_bits}", _keccak(digest_bits), digest_bits//8)
    return True
