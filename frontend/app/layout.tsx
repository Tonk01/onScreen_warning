import "./globals.css";

export const metadata = {
  title: "Onscreen",
  description: "Public transport service alerts",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en">
      <body> {children} </body>
    </html>
  );
}
