#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>

int main()
{
  sf::RenderWindow window(sf::VideoMode(800, 400), "SFML works!", sf::Style::Default);
  window.setFramerateLimit(60);

  sf::CircleShape circle(50.f);
  circle.setPosition(sf::Vector2f(0.f, 0.f));
  circle.setFillColor(sf::Color(255, 100, 200, 200));

  sf::RectangleShape rect(sf::Vector2f(50.0f, 100.0f));
  rect.setPosition(sf::Vector2f(400.f, 200.f));
  rect.setFillColor(sf::Color(255, 255, 200, 100));

  while (window.isOpen())
  {
    sf::Event event;
    while (window.pollEvent(event))
    {
      if (event.type == sf::Event::Closed)
        window.close();
    }

    // circle.move(0.5f, 0.1f);
    // circle.rotate(2.0f);

    // rect.move(-0.5f, -0.1f);
    // rect.rotate(5.0f);

    //Desenhar
    window.clear(sf::Color::Blue);
    window.draw(circle);
    window.draw(rect);

    window.display();
  }

  return 0;
}
