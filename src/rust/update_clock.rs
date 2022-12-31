use std::process::Command;

struct DateTime {
    year: String,
    month: String,
    day: String,
    hour: String,
    minute: String,
    second: String,
}

impl DateTime {
    fn get_month_from_str(month_str: &str) -> &str {
        let month_value = match month_str {
            "Jan" => "01",
            "Feb" => "02",
            "Mar" => "03",
            "Apr" => "04",
            "May" => "05",
            "Jun" => "06",
            "Jul" => "07",
            "Aug" => "08",
            "Sep" => "09",
            "Oct" => "10",
            "Nov" => "11",
            "Dec" => "12",
            _ => panic!("Month name not recognized"),
        };

        return month_value;
    }

    fn from(date_str: &str) -> DateTime {
        let date_params: Vec<&str> = date_str.split(' ').collect();
        let day = date_params[1];
        let month = DateTime::get_month_from_str(date_params[2]);
        let year_bytes = u8::from_str_radix(date_params[3], 10).expect("Failed to parse") - 3;
        let year = String::from(format!("{year_bytes}"));

        let time_params: Vec<&str> = date_params[4].split(':').collect();
        let hour = time_params[0];
        let minute = time_params[1];
        let second = time_params[2];

        return DateTime {
            year: String::from(year),
            month: String::from(month),
            day: String::from(day),
            hour: String::from(hour),
            minute: String::from(minute),
            second: String::from(second),
        };
    }

    fn parse(&self) -> String {
        let year = &self.year;
        let month = &self.month;
        let day = &self.day;
        let hour = &self.hour;
        let minute = &self.minute;
        let second = &self.second;
        let date_string = format!("{year}-{month}-{day}");
        let time_string = format!("{hour}:{minute}:{second}");
        let date_time_string = format!("{date_string} {time_string}");
        return date_time_string;
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let google_response = reqwest::get("https://www.google.com")
        .await?;

    let google_headers = google_response.headers();
    let date_result = google_headers.get("date").unwrap().to_str();
    let date_str = match date_result {
        Ok(value) => value,
        Err(error) => panic!("{:?}", error),
    };

    let date_object = DateTime::from(date_str);
    let date_time = date_object.parse();

    Command::new("timedatectl")
        .args(["set-ntp", "false"])
        .output()
        .expect("Failed to set system time");

    Command::new("timedatectl")
        .args(["set-time", date_time.as_str()])
        .output()
        .expect("Failed to set system time");

    Command::new("timedatectl")
        .args(["set-ntp", "true"])
        .output()
        .expect("Failed to set system time");

    Ok(())
}
