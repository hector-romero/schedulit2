class AuthToken < ApplicationRecord
  belongs_to :user

  self.primary_key = :digest
  self.table_name = 'knox_authtoken'

  def token
    @_token
  end

  before_create :initialize_token
  private

  def initialize_token
    @_token = KnoxToken.create_token_string

    self[:digest] = KnoxToken.hash_token(@_token)
    self[:token_key] = KnoxToken.token_key(@_token)
  end

  class << self
    private

    def timestamp_attributes_for_create
      super << 'created'
    end
  end
end
