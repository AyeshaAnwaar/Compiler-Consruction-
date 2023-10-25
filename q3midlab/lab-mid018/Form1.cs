using System;
using System.Reflection.Emit;
using System.Text;
using System.Windows.Forms; // Make sure to include the Windows Forms namespace.

namespace lab_mid018
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string firstName = textBox1.Text; // Assuming you have text boxes for first name and last name initials.
            string lastName = textBox2.Text;

            if (int.TryParse(textBox3.Text, out int passwordLength))
            {
                if (passwordLength > 16)
                {
                    passwordLength = 16; // Limit the password length to 16 characters.
                }

                string generatedPassword = GeneratePassword(firstName, lastName, passwordLength);
                label4.Text = generatedPassword;
            }
            else
            {
                label4.Text = "Invalid password length. Please provide a valid number.";
            }
        }

        private string GeneratePassword(string firstName, string lastName, int passwordLength)
        {
            Random random = new Random();
            StringBuilder password = new StringBuilder();

            // Add the initials of the first and last name.
            password.Append(char.ToUpper(firstName[0]));
            password.Append(char.ToUpper(lastName[0]));

            // Generate at least one uppercase alphabet.
            password.Append((char)(random.Next(26) + 'A'));

            // Generate at least 4 numbers (two of which are '18').
            for (int i = 0; i < 2; i++)
            {
                password.Append('1');
                password.Append('8');
            }
            for (int i = 0; i < passwordLength - password.Length; i++)
            {
                password.Append((char)(random.Next(10) + '0'));
            }

            // Generate at least 2 special characters.
            string specialCharacters = "!@#$%^&*()_+-=";
            for (int i = 0; i < 2; i++)
            {
                password.Append(specialCharacters[random.Next(specialCharacters.Length)]);
            }

            // Shuffle the characters to randomize the order.
            for (int i = password.Length - 1; i > 0; i--)
            {
                int j = random.Next(i + 1);
                char temp = password[i];
                password[i] = password[j];
                password[j] = temp;
            }

            return password.ToString();
        }
    }
}