class Shift < ApplicationRecord
  belongs_to :employee, class_name: 'User'

  self.table_name = 'shift_shift'

  class << self
    private

    def timestamp_attributes_for_create
      super << 'timestamp'  # Todo Rename field to created_at in the django app
    end
  end

end
