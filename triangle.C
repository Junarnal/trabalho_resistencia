#include <iostream>
#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>

int main()
{
  sf::RenderWindow window(sf::VideoMode(640, 400), "Triangles and lines");
  window.setFramerateLimit(60);

  sf::CircleShape triangle;
  triangle.setRadius(100.f);
  triangle.setPointCount(3);
  triangle.setOutlineThickness(3.f);
  triangle.setOutlineColor(sf::Color::Blue);

  sf::Vertex line[] = {sf::Vertex(sf::Vector2f(100.f, 400.f)), sf::Vertex(sf::Vector2f(50.0f, 100.0f))};

  sf::ConvexShape triangle_rect;
  triangle_rect.setPointCount(3);
  triangle_rect.setPoint(0, sf::Vector2f(200.f, 200.f));
  triangle_rect.setPoint(1, sf::Vector2f(250.f, 300.f));
  triangle_rect.setPoint(2, sf::Vector2f(200.f, 300.f));

  while(window.isOpen())
 
  {
    sf::Event event;
    while(window.pollEvent(event))
    {
      if(event.type == sf::Event::Closed)
        window.close();
    }

    window.clear(sf::Color(72, 77, 80, 0));
    
    window.draw(triangle);
    window.draw(line, 2, sf::Lines);
    window.draw(triangle_rect);

    window.display();
  }
  return 0;
}

