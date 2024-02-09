document.addEventListener('DOMContentLoaded', function() {
    // make send otp request 
    var sendOtpButton = document.getElementById('send-otp');
    var otpDiv = document.getElementById('otp-div');
    
    sendOtpButton.addEventListener('click', function() {
    
        var email = document.querySelector('input[name="email"]').value;
        // AJAX call to perform send otp functionality
        var xhr = new XMLHttpRequest();
        xhr.open('GET', '/api/sent-otp/?email=' + email, true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.status === 'success') {
                    alert('Otp Sent Successfully');
                    // Clear otp-div
                    otpDiv.innerHTML = '';
    
                    // Create OTP input field
                    var otpInput = document.createElement('input');
                    otpInput.type = 'text';
                    otpInput.name = 'otp';
                    otpInput.placeholder = 'Enter OTP';
                    otpInput.required = true;
    
                    // Create verify OTP button
                    var verifyOtpButton = document.createElement('button');
                    verifyOtpButton.textContent = 'Verify OTP';
                    verifyOtpButton.className = 'main-btn primary-btn btn-hover w-100 text-center mt-2';
                    
                    verifyOtpButton.addEventListener('click', function() {
                        // Code to verify OTP
                        var otp = document.querySelector('input[name="otp"]').value;
                        var xhr = new XMLHttpRequest();
                        xhr.open('GET', '/api/forget-pass/?email=' + email + '&otp=' + otp, true);
                        xhr.onreadystatechange = function() {
                            var response = JSON.parse(xhr.responseText);
                            if (response.status === 'success') {
                                
                            }else{
    
                            }
                        }
                        
                    });
    
                    // Append OTP input field and verify OTP button to otp-div
                    otpDiv.appendChild(otpInput);
                    otpDiv.appendChild(verifyOtpButton);
    
                    // Hide send OTP button
                    sendOtpButton.style.display = 'none';
                } else {
                    // Something went wrong
                    alert(response.status);
                    window.location.reload();
                }
            }
        };
        xhr.send();
    });
    
    
    
    });