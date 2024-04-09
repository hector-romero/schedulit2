class AuthToken < ApplicationRecord
  belongs_to :user

  self.primary_key = :digest
  self.table_name = 'knox_authtoken'

  class << self
    private

    def timestamp_attributes_for_create
      super << 'created'
    end
  end
end
