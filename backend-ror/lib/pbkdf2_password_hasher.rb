require 'openssl'
require "base64"
require 'securerandom'


# Since I want to use the same database used for the django application, I will implement the same password hashing
# algorithm for authentication in rails that is used as default for django (PBKDF2):
# class PBKDF2PasswordHasher(BasePasswordHasher):
#     """
#     Secure password hashing using the PBKDF2 algorithm (recommended)
#
#     Configured to use PBKDF2 + HMAC + SHA256.
#     The result is a 64 byte binary string.  Iterations may be changed
#     safely but you must rename the algorithm if you change SHA256.
#     """
#
#     algorithm = "pbkdf2_sha256"
#     iterations = 720000
#     digest = hashlib.sha256
#
#     def encode(self, password, salt, iterations=None):
#         self._check_encode_args(password, salt)
#         iterations = iterations or self.iterations
#         hash = pbkdf2(password, salt, iterations, digest=self.digest)
#         hash = base64.b64encode(hash).decode("ascii").strip()
#         return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)
#
#     def decode(self, encoded):
#         algorithm, iterations, salt, hash = encoded.split("$", 3)
#         assert algorithm == self.algorithm
#         return {
#             "algorithm": algorithm,
#             "hash": hash,
#             "iterations": int(iterations),
#             "salt": salt,
#         }
#
#     def verify(self, password, encoded):
#         decoded = self.decode(encoded)
#         encoded_2 = self.encode(password, decoded["salt"], decoded["iterations"])
#         return constant_time_compare(encoded, encoded_2)
#
#     def safe_summary(self, encoded):
#         decoded = self.decode(encoded)
#         return {
#             _("algorithm"): decoded["algorithm"],
#             _("iterations"): decoded["iterations"],
#             _("salt"): mask_hash(decoded["salt"]),
#             _("hash"): mask_hash(decoded["hash"]),
#         }
#
#     def must_update(self, encoded):
#         decoded = self.decode(encoded)
#         update_salt = must_update_salt(decoded["salt"], self.salt_entropy)
#         return (decoded["iterations"] != self.iterations) or update_salt
#
#     def harden_runtime(self, password, encoded):
#         decoded = self.decode(encoded)
#         extra_iterations = self.iterations - decoded["iterations"]
#         if extra_iterations > 0:
#             self.encode(password, decoded["salt"], extra_iterations)
#

Password = Struct.new(:algorithm, :iterations, :salt, :hash) do
    def to_s
        "#{algorithm}$#{iterations}$#{salt}$#{hash}"
    end

    def self.decode(encoded)
        parts = encoded.split("$", 4)
        algorithm = parts[0]
        iterations = parts[1]
        salt = parts[2]
        hash = parts[3]
        Password.new(algorithm, iterations.to_i, salt, hash)
    end
end


module Pbkdf2PasswordHasher
    ITERATIONS = 720000
    ALGORITHM = "pbkdf2_sha256"
    SALT_LENGTH = 22

    def self.salt
      SecureRandom.alphanumeric(Pbkdf2PasswordHasher::SALT_LENGTH)
    end

    def self.encode(password, salt = nil, iterations=nil)
        unless iterations
            iterations = Pbkdf2PasswordHasher::ITERATIONS
        end

        unless salt
            salt = self.salt
        end

        digest = OpenSSL::Digest::SHA256.new
        # the final value to be stored
        hash = OpenSSL::KDF.pbkdf2_hmac(password, salt: salt, iterations: iterations,
                                         length: digest.digest_length, hash: digest)
        hash = Base64.strict_encode64(hash).to_s.strip
        Password.new(Pbkdf2PasswordHasher::ALGORITHM, iterations, salt, hash).to_s
    end

    def self.verify(password, encoded)
        decoded = Password.decode(encoded)
        encoded_2 = self.encode(password, decoded.salt, decoded.iterations)
        return OpenSSL.fixed_length_secure_compare(encoded, encoded_2)
    end
end
