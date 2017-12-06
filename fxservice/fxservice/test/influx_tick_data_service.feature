Feature: Influx_tick_data_service
  Kiểm tra

  Scenario: Tạo service với db mới thì dữ liệu là mặc định
    Given Tạo service test với db mới
    Then Kiểm tra count bằng 0
    Then Kiểm tra lasted bar bằng None

  Scenario: Tạo service với db mới và thêm dữ liệu thì thêm đúng
    Given Tạo service test với db mới
    And Thêm 1 tick
    Then Kiểm tra count bằng 1
    Then Kiểm tra lasted bar khác None