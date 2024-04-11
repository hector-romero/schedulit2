class AuthToken < ApplicationRecord
  belongs_to :user

  self.primary_key = :digest
  self.table_name = 'knox_authtoken'

  before_create :initialize_token

  def token
    @_token
  end

  private

  def initialize_token
    @_token = KnoxToken.create_token_string

    self[:digest] = KnoxToken.hash_token(@_token)
    self[:token_key] = KnoxToken.token_key(@_token)
  end

  def self.get_by_token(token)
    token_key = KnoxToken.token_key(token)
    auth_token = AuthToken.find_by(token_key: token_key)
    unless auth_token and KnoxToken.compare_digest(token, auth_token.digest)
      return nil
    end
    auth_token
  end

  class << self
    private

    def timestamp_attributes_for_create
      super << 'created'
    end
  end
end
