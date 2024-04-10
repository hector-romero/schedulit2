class User < ApplicationRecord
  attribute :is_superuser, :boolean, default: false
  attribute :is_staff, :boolean, default: false
  attribute :is_active, :boolean, default: true
  attribute :employee_id, :string, default: ''
  attribute :name, :string, default: ''
  # https://edgeapi.rubyonrails.org/classes/ActiveRecord/Enum.html
  enum :role, {scheduler: 'scheduler', employee: 'employee'}, default: :scheduler

  self.table_name = 'authentication_user'

  # before_create :set_date_joined
  # before_save :set_date_joined
  #
  # # private
  # def set_date_joined
  #   self.date_joined = DateTime.now
  # end
  def password
    self[:password]
  end

  def password=(raw_password)
    self[:password] = Pbkdf2PasswordHasher.encode(raw_password)
  end

  def check_password(raw_password)
    """
        Return a boolean of whether the raw_password was correct
    """
    Pbkdf2PasswordHasher.verify(raw_password, self[:password])
  end

  class << self
    private

    def timestamp_attributes_for_create
      super << 'date_joined'
    end
  end

end
