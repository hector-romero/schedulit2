class User < ApplicationRecord
  # has_many :authtokens, foreign_key: 'user_id', class_name: 'Authtoken'

  self.table_name = 'authentication_user'

  # before_create :set_date_joined
  # before_save :set_date_joined
  #
  # # private
  # def set_date_joined
  #   self.date_joined = DateTime.now
  # end
  class << self
    private

    def timestamp_attributes_for_create
      super << 'date_joined'
    end
  end

end
