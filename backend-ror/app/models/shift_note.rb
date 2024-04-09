class ShiftNote < ApplicationRecord
  belongs_to :shift

  self.table_name = 'shift_shiftnote'

  class << self
    private

    def timestamp_attributes_for_create
      super << 'timestamp'  # Todo Rename field to created_at in the django app
    end
  end

end
