# Module based on the plugin django-rest-knox used to provide authentication tokens for users
# https://github.com/jazzband/django-rest-knox/
# https://github.com/jazzband/django-rest-knox/blob/master/knox/
# Initially, I will not support any of the options of knox. It will be just a token with no expiration date
require 'securerandom'
require 'binascii'

module KnoxToken
  AUTH_TOKEN_CHARACTER_LENGTH = 64  # Matches django_settings
  TOKEN_KEY_LENGTH = 8

  def self.create_token_string
      SecureRandom.hex(KnoxToken::AUTH_TOKEN_CHARACTER_LENGTH / 2)
  end

  def self.hash_token(token)
    '''
    Calculates the hash of a token.
    input is unhexlified (using binascii)

    token must contain an even number of hex digits or a binascii.Error
    exception will be raised
    Forcing the use of hasher SHA512 from knox_settings.SECURE_HASH_ALGORITHM
    '''
    OpenSSL::Digest::SHA512.hexdigest(Binascii.unhexlify(token))
  end

  def self.token_key(token)
    '''
      Trims the token to the TOKEN_KEY_LENGTH
    '''
    token[0..KnoxToken::TOKEN_KEY_LENGTH - 1]
  end

  def self.compare_digest(token, digest)
    token_digest = self.hash_token(token)
    return token_digest == digest
  end
end
